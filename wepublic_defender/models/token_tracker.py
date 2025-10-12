from datetime import datetime
from typing import (
    Optional,
    Dict,
    List,
    Tuple,
    Union,
    Any,
    Iterator,
    Literal,
    Generic,
    TypeVar,
    Iterable,
    overload,
)
from pydantic import BaseModel, Field
import time

try:
    from rich.table import Table
    from rich.console import Console

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# ── TokenUsage ─────────────────────────────────────────────────────────────────
class TokenUsage(BaseModel):
    model: Optional[str] = Field(default=None)
    effort: Optional[Literal["minimal", "low", "medium", "high", None]] = None
    input: int = 0
    output: int = 0
    cached: int = 0
    notes: Optional[str] = None
    duration: Optional[float] = Field(
        default=None, description="Duration of the api call in seconds"
    )
    service_tier: Literal["auto", "flex", "standard", "priority"] = "auto"
    timestamp: float = Field(default_factory=time.time)
    # Image/PDF metadata
    image_count: Optional[int] = Field(
        default=None, description="Number of images sent with the API call"
    )
    image_total_bytes: Optional[int] = Field(
        default=None, description="Total size of all images in bytes"
    )
    image_format: Optional[str] = Field(
        default=None, description="Format of images sent (e.g., 'jpeg', 'pdf')"
    )

    def local_time(self, fmt="%Y-%m-%d %H:%M:%S") -> str:
        return datetime.fromtimestamp(self.timestamp).astimezone().strftime(fmt)

    def add(self, inp: int, out: int, cache: int = 0) -> None:
        self.input += inp
        self.output += out
        self.cached += cache

    @property
    def total(self) -> int:
        return self.input + self.output - self.cached

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenUsage):
            return False
        return (
            self.model == other.model
            and self.input == other.input
            and self.output == other.output
            and self.cached == other.cached
            and self.notes == other.notes
            and self.service_tier == other.service_tier
            and self.duration == other.duration
            and self.timestamp == other.timestamp
        )

    def __bool__(self) -> bool:
        return self.model is not None and self.input > 0 and self.output > 0


class TokenTracker:
    """Track token usage for multiple models."""

    def __init__(self, models_config: Dict[str, Dict[str, float]]):
        """Initialize with a configuration of models and their token costs.

        Args:
            models_config: A dictionary mapping model names to their token costs.
        """
        self.cfg = models_config
        self._usage: Dict[str, TokenUsage] = {}
        self._history: list[TokenUsage] = []  # <- keep every individual entry

    # ----- ingest --------------------------------------------------------------
    def add(
        self,
        model: str,
        inp: int,
        out: int,
        cache: int = 0,
        effort: Literal["minimal", "low", "medium", "high", None] = None,
        notes: str | None = None,
        service_tier: Literal["auto", "flex", "standard", "priority"] = "auto",
        duration: Optional[float] = None,
        timestamp: Optional[float] = None,
        image_count: Optional[int] = None,
        image_total_bytes: Optional[int] = None,
        image_format: Optional[str] = None,
    ) -> None:
        """Record a single usage event.

        Args:
            model: The name of the model used (e.g., "gpt-4.1").
            effort: The effort level of the model used (e.g., "low").
            inp: The number of input tokens.
            out: The number of output tokens.
            cache: The number of cached tokens.
            notes: Optional notes about the usage event.
            timestamp: Optional timestamp for the usage event.
        """
        event = TokenUsage(
            model=model,
            effort=effort,
            input=inp,
            output=out,
            cached=cache,
            notes=notes,
            service_tier=service_tier,
            duration=duration,
            timestamp=timestamp or time.time(),
            image_count=image_count,
            image_total_bytes=image_total_bytes,
            image_format=image_format,
        )
        if not event:
            return
        # make sure we haven't already added this usage event
        if event in self._history:
            return

        # keep full history
        self._history.append(event)

        # update simple per-model totals (no extra bookkeeping)
        # Preserve service_tier from most recent event for aggregated usage
        agg = self._usage.setdefault(model, TokenUsage(model=model))
        agg.add(inp, out, cache)
        if service_tier:
            agg.service_tier = service_tier

    # convenience wrapper
    def add_usage(self, usage: TokenUsage) -> None:
        """Add a usage event to the tracker."""
        if not usage:
            return
        self.add(
            model=usage.model,
            effort=usage.effort,
            inp=usage.input,
            out=usage.output,
            cache=usage.cached,
            notes=usage.notes,
            service_tier=usage.service_tier,
            duration=usage.duration,
            timestamp=usage.timestamp,
            image_count=usage.image_count,
            image_total_bytes=usage.image_total_bytes,
            image_format=usage.image_format,
        )

    def add_usages(self, usages: list[TokenUsage]) -> None:
        """Add multiple usage events to the tracker."""
        for usage in usages:
            self.add_usage(usage)

    def clear(self) -> None:
        """Clear all usage data."""
        self._usage.clear()
        self._history.clear()

    # ── internals ─────────────────────────────────────────────────────────────────
    def _cost(self, model: str, u: TokenUsage) -> Tuple[float, float, float, float, float]:
        cfg = self.cfg[model]

        # Determine pricing based on service tier and model configuration
        if u.service_tier == "priority" and "priority_tier" in cfg:
            # Use explicit priority tier pricing (OpenAI models)
            ic = cfg["priority_tier"]["input_token_ppm"]
            cc = cfg["priority_tier"]["input_token_cached_ppm"]
            oc = cfg["priority_tier"]["output_token_ppm"]
        elif "tiered_pricing" in cfg:
            # Handle context-based tiered pricing (e.g., grok-4-fast)
            total_tokens = u.input + u.output
            threshold = cfg["tiered_pricing"]["threshold_tokens"]
            if total_tokens <= threshold:
                tier = cfg["tiered_pricing"]["under_threshold"]
            else:
                tier = cfg["tiered_pricing"]["over_threshold"]
            ic = tier["input_token_ppm"]
            cc = tier["input_token_cached_ppm"]
            oc = tier["output_token_ppm"]
        else:
            # Standard pricing with service tier multipliers
            if u.service_tier == "flex":
                factor = 0.5
            elif u.service_tier == "priority":
                # Fallback to priority_multiplier if priority_tier not available
                factor = cfg.get("priority_multiplier", 2.0)
            else:
                factor = 1.0

            ic = cfg["input_token_ppm"] * factor
            cc = cfg.get("input_token_cached_ppm", cfg["input_token_ppm"] / 2) * factor
            oc = cfg["output_token_ppm"] * factor

        # Calculate costs
        in_cost = (u.input - u.cached) * ic / 1_000_000
        cache_cost = u.cached * cc / 1_000_000
        # For saved cost, compare against base input price (not cached price)
        base_ic = cfg["input_token_ppm"]
        saved_cost = u.cached * (base_ic - cc) / 1_000_000
        out_cost = u.output * oc / 1_000_000
        total_cost = in_cost + cache_cost + out_cost
        return in_cost, cache_cost, out_cost, total_cost, saved_cost

    # ── usage / cost helpers (signatures unchanged) ───────────────────────────────
    def cost(self, model: str) -> Tuple[float, float, float, float, float]:
        """Return the cost of a model's usage.

        Args:
            model: The name of the model used (e.g., "gpt-4.1").

        Returns:
            A tuple of (input_cost, cache_cost, out_cost, total_cost, saved_cost).
        """
        return self._cost(model, self.usage(model))

    def cost_all(self) -> Dict[str, Tuple[float, float, float, float, float]]:
        """Return the cost of all models' usage.

        Returns:
            A dictionary mapping model names to their costs.
        """
        return {m: self.cost(m) for m in self._usage}

    def cost_for_usage(self, usage: TokenUsage) -> Tuple[float, float, float, float, float]:
        """Return the cost of a specific usage event.

        Args:
            usage: The usage event to calculate the cost for.

        Returns:
            A tuple of (input_cost, cache_cost, out_cost, total_cost, saved_cost).
        """
        return self._cost(usage.model, usage)

    def usage(self, model: str) -> TokenUsage:
        """Return the usage for a specific model."""
        return self._usage.get(model, TokenUsage(model=model))

    def usage_total(self) -> TokenUsage:
        """Return the total usage for all models."""
        return TokenUsage(
            model="ALL",
            input=sum(u.input for u in self._usage.values()),
            output=sum(u.output for u in self._usage.values()),
            cached=sum(u.cached for u in self._usage.values()),
        )

    # ── Timeline calculation methods ────────────────────────────────────────────
    def calculate_wall_clock_time(self) -> float:
        """Calculate actual wall-clock time from overlapping operations.

        This handles parallel operations by:
        1. Converting each usage to a time segment (start, end)
        2. Merging overlapping segments
        3. Summing the non-overlapping segments

        Note: timestamp represents when the operation completed (end time)

        Returns:
            Total wall-clock time in seconds
        """
        # Build list of time segments (start, end) from history
        segments = []
        for usage in self._history:
            if usage.timestamp is not None and usage.duration is not None:
                end = usage.timestamp  # timestamp is when the operation completed
                start = usage.timestamp - usage.duration  # start is duration before end
                segments.append((start, end))

        if not segments:
            return 0.0

        # Sort segments by start time
        segments.sort(key=lambda x: x[0])

        # Merge overlapping segments
        merged = []
        current_start, current_end = segments[0]

        for start, end in segments[1:]:
            if start <= current_end:
                # Overlapping segment - extend the current segment
                current_end = max(current_end, end)
            else:
                # Non-overlapping segment - save current and start new
                merged.append((current_start, current_end))
                current_start, current_end = start, end

        # Don't forget the last segment
        merged.append((current_start, current_end))

        # Calculate total wall-clock time
        wall_clock_time = sum(end - start for start, end in merged)

        return wall_clock_time

    def calculate_parallelism_metrics(self) -> Dict[str, float]:
        """Calculate detailed parallelism metrics from token usage.

        Returns:
            Dictionary with:
            - wall_clock_time: Actual elapsed time
            - compute_time: Sum of all operation durations
            - parallelism_factor: compute_time / wall_clock_time
            - overlap_percentage: How much time was spent in parallel
            - max_concurrent: Maximum number of concurrent operations
        """
        wall_clock = self.calculate_wall_clock_time()
        compute_time = sum(u.duration for u in self._history if u.duration is not None)

        if wall_clock == 0:
            return {
                "wall_clock_time": 0.0,
                "compute_time": compute_time,
                "parallelism_factor": 0.0,
                "overlap_percentage": 0.0,
                "max_concurrent": 0,
            }

        # Calculate max concurrent operations
        events = []
        for usage in self._history:
            if usage.timestamp is not None and usage.duration is not None:
                start = usage.timestamp - usage.duration  # Start is duration before end
                end = usage.timestamp  # timestamp is when the operation completed
                events.append((start, 1))  # Start event
                events.append((end, -1))  # End event

        events.sort()
        current_concurrent = 0
        max_concurrent = 0

        for _, delta in events:
            current_concurrent += delta
            max_concurrent = max(max_concurrent, current_concurrent)

        # Calculate overlap percentage
        # This is the percentage of time where >1 operation was running
        if len(self._history) <= 1:
            overlap_pct = 0.0
        else:
            # Calculate time spent with exactly 1 operation
            single_op_time = 0.0
            last_time = None
            current_concurrent = 0

            for time, delta in events:
                if last_time is not None and current_concurrent == 1:
                    single_op_time += time - last_time
                current_concurrent += delta
                last_time = time

            overlap_pct = (
                ((wall_clock - single_op_time) / wall_clock * 100) if wall_clock > 0 else 0.0
            )

        return {
            "wall_clock_time": wall_clock,
            "compute_time": compute_time,
            "parallelism_factor": compute_time / wall_clock if wall_clock > 0 else 0.0,
            "overlap_percentage": overlap_pct,
            "max_concurrent": max_concurrent,
        }

    # ── reports ------------------------------------------------------------------
    def report(self) -> str:
        """Return a report of the token usage."""
        # Try to use rich table if available
        if RICH_AVAILABLE:
            try:
                from rich.console import Console

                console = Console()
                table = self.report_rich()
                with console.capture() as capture:
                    console.print(table)
                return capture.get()
            except:
                pass  # Fall back to text report

        # Original text report
        lines = []
        total_duration = 0.0

        # Calculate costs per model from the detailed history (to preserve service tier pricing)
        model_costs = {}
        for u in self._history:
            if u.duration is not None:
                total_duration += u.duration

            # Calculate cost for this specific usage with its service tier
            ic, cc, oc, tc, sv = self._cost(u.model, u)

            if u.model not in model_costs:
                model_costs[u.model] = {
                    "in": 0.0,
                    "cache": 0.0,
                    "out": 0.0,
                    "total": 0.0,
                    "saved": 0.0,
                }

            model_costs[u.model]["in"] += ic
            model_costs[u.model]["cache"] += cc
            model_costs[u.model]["out"] += oc
            model_costs[u.model]["total"] += tc
            model_costs[u.model]["saved"] += sv

        # Build report lines
        grand = 0.0
        saved = 0.0
        for model, costs in model_costs.items():
            lines.append(
                f"{model:<15} total ${costs['total']:.6f} | in ${costs['in']:.6f} | cache ${costs['cache']:.6f} "
                f"| out ${costs['out']:.6f} | saved ${costs['saved']:.6f}"
            )
            grand += costs["total"]
            saved += costs["saved"]

        lines.append("-" * 88)

        # Calculate parallelism metrics
        metrics = self.calculate_parallelism_metrics()
        wall_clock = metrics["wall_clock_time"]

        # Show both wall-clock and compute time
        if total_duration > 0:
            if wall_clock > 0 and wall_clock < total_duration:
                # Parallel processing detected
                dur_str = f" | wall-clock {wall_clock:.1f}s | compute {total_duration:.1f}s ({metrics['parallelism_factor']:.1f}x parallel)"
            else:
                # Sequential or no parallelism detected
                dur_str = f" | duration {total_duration:.1f}s"
        else:
            dur_str = ""

        lines.append(f"ALL MODELS       total ${grand:.6f} | saved ${saved:.6f}{dur_str}")
        return "\n".join(lines)

    def report_for_usage(self, usage: TokenUsage) -> str:
        """Return a report for a specific usage event."""
        ic, cc, oc, tc, sv = self.cost_for_usage(usage)
        t = usage.local_time()
        return (
            f"{t} | {usage.model:<15} total ${tc:.6f} | in ${ic:.6f} "
            f"| cache ${cc:.6f} | out ${oc:.6f} | saved ${sv:.6f}"
        )

    def report_detail(self, sort_by: str = "time", desc: bool = False) -> str:  # "time" | "cost"
        """Return a detailed report of the token usage."""
        # Try to use rich table if available
        if RICH_AVAILABLE:
            try:
                from rich.console import Console

                console = Console()
                table = self.report_detail_rich(sort_by=sort_by, desc=desc)
                with console.capture() as capture:
                    console.print(table)
                return capture.get()
            except:
                pass  # Fall back to text report

        # Original text report
        rows, tot_in, tot_out, tot_cache, tot_cost, tot_saved, tot_duration = (
            [],
            0,
            0,
            0,
            0.0,
            0.0,
            0.0,
        )

        for u in self._history:
            ic, cc, oc, tc, sv = self._cost(u.model, u)
            rows.append((u, u.timestamp, tc, sv))
            tot_in += u.input
            tot_out += u.output
            tot_cache += u.cached
            tot_cost += tc
            tot_saved += sv
            if u.duration is not None:
                tot_duration += u.duration

        key_fn = (lambda r: r[2]) if sort_by == "cost" else (lambda r: r[1])
        rows.sort(key=key_fn, reverse=desc)

        lines = []
        for r in rows:
            mpe = r[0].model
            if getattr(r[0], "effort", None) and (
                r[0].model.startswith("o") or r[0].model.startswith("gpt-5")
            ):
                mpe = f"{r[0].model}.{r[0].effort}"
            # Include duration if available, formatted to 1 decimal place
            dur_str = (
                f" | dur {r[0].duration:.1f}s"
                if getattr(r[0], "duration", None) is not None
                else ""
            )
            lines.append(
                f"{r[0].local_time()} | {mpe:<19} "
                f"in {r[0].input:>6} | out {r[0].output:>6} | "
                f"cache {r[0].cached:>6} | cost ${self._cost(r[0].model, r[0])[3]:.6f} "
                f"| saved ${r[3]:.6f}{dur_str} | tier {r[0].service_tier} | notes: {r[0].notes or '-'}"
            )

        lines.append("-" * 110)

        # Calculate parallelism metrics
        metrics = self.calculate_parallelism_metrics()
        wall_clock = metrics["wall_clock_time"]

        # Show both wall-clock and compute time
        if tot_duration > 0:
            if wall_clock > 0 and wall_clock < tot_duration:
                # Parallel processing detected
                dur_str = f" | wall {wall_clock:.1f}s | compute {tot_duration:.1f}s ({metrics['parallelism_factor']:.1f}x)"
            else:
                # Sequential or no parallelism detected
                dur_str = f" | duration {tot_duration:.1f}s"
        else:
            dur_str = ""

        lines.append(
            f"TOTALS{'':12} "
            f"in {tot_in:>6} | out {tot_out:>6} | "
            f"cache {tot_cache:>6} | cost ${tot_cost:.6f} | saved ${tot_saved:.6f}{dur_str}"
        )
        return "\n".join(lines)

    # ── Rich table reports ───────────────────────────────────────────────────────
    def report_rich(self, console: Optional["Console"] = None) -> Union["Table", str]:
        """Return a rich table report of the token usage.

        Args:
            console: Optional Rich Console instance. If provided, prints the table.
                    If None, returns the table object.

        Returns:
            Rich Table object if console is None, otherwise returns string version.
        """
        if not RICH_AVAILABLE:
            return self.report()  # Fallback to text report

        table = Table(title="Token Usage Summary", show_footer=True)
        table.add_column("Model", footer="ALL MODELS", style="cyan", no_wrap=True)
        table.add_column("Total Cost", footer="", justify="right", style="green")
        table.add_column("Input Cost", footer="", justify="right")
        table.add_column("Cache Cost", footer="", justify="right")
        table.add_column("Output Cost", footer="", justify="right")
        table.add_column("Saved", footer="", justify="right", style="yellow")

        total_duration = 0.0
        model_costs = {}

        # Calculate costs per model from the detailed history
        for u in self._history:
            if u.duration is not None:
                total_duration += u.duration

            ic, cc, oc, tc, sv = self._cost(u.model, u)

            if u.model not in model_costs:
                model_costs[u.model] = {
                    "in": 0.0,
                    "cache": 0.0,
                    "out": 0.0,
                    "total": 0.0,
                    "saved": 0.0,
                }

            model_costs[u.model]["in"] += ic
            model_costs[u.model]["cache"] += cc
            model_costs[u.model]["out"] += oc
            model_costs[u.model]["total"] += tc
            model_costs[u.model]["saved"] += sv

        grand = 0.0
        saved = 0.0

        # Add rows for each model
        for model, costs in model_costs.items():
            table.add_row(
                model,
                f"${costs['total']:.6f}",
                f"${costs['in']:.6f}",
                f"${costs['cache']:.6f}",
                f"${costs['out']:.6f}",
                f"${costs['saved']:.6f}",
            )
            grand += costs["total"]
            saved += costs["saved"]

        # Calculate parallelism metrics
        metrics = self.calculate_parallelism_metrics()
        wall_clock = metrics["wall_clock_time"]

        # Update footer with totals
        if total_duration > 0:
            if wall_clock > 0 and wall_clock < total_duration:
                # Parallel processing detected
                dur_str = f" (wall {wall_clock:.1f}s, compute {total_duration:.1f}s, {metrics['parallelism_factor']:.1f}x)"
            else:
                # Sequential or no parallelism detected
                dur_str = f" ({total_duration:.1f}s)"
        else:
            dur_str = ""

        table.columns[1].footer = f"${grand:.6f}{dur_str}"
        table.columns[5].footer = f"${saved:.6f}"

        if console:
            console.print(table)
            return self.report()  # Return text version for compatibility
        return table

    def report_detail_rich(
        self, sort_by: str = "time", desc: bool = False, console: Optional["Console"] = None
    ) -> Union["Table", str]:
        """Return a rich table detailed report of the token usage.

        Args:
            sort_by: Sort by "time" or "cost"
            desc: Sort in descending order
            console: Optional Rich Console instance. If provided, prints the table.
                    If None, returns the table object.

        Returns:
            Rich Table object if console is None, otherwise returns string version.
        """
        if not RICH_AVAILABLE:
            return self.report_detail(sort_by=sort_by, desc=desc)  # Fallback

        table = Table(title="Token Usage Details", show_footer=True)
        table.add_column("Timestamp", footer="TOTALS", style="dim")
        table.add_column("Model", footer="", style="cyan", no_wrap=True)
        table.add_column("Input", footer="", justify="right")
        table.add_column("Output", footer="", justify="right")
        table.add_column("Cache", footer="", justify="right", style="dim")
        table.add_column("Cost", footer="", justify="right", style="green")
        table.add_column("Saved", footer="", justify="right", style="yellow")
        table.add_column("Duration", footer="", justify="right", style="magenta")
        table.add_column("Tier", footer="", style="blue")
        table.add_column("Notes", footer="", style="dim", overflow="fold")

        rows = []
        tot_in, tot_out, tot_cache = 0, 0, 0
        tot_cost, tot_saved, tot_duration = 0.0, 0.0, 0.0

        for u in self._history:
            ic, cc, oc, tc, sv = self._cost(u.model, u)
            rows.append((u, u.timestamp, tc, sv))
            tot_in += u.input
            tot_out += u.output
            tot_cache += u.cached
            tot_cost += tc
            tot_saved += sv
            if u.duration is not None:
                tot_duration += u.duration

        key_fn = (lambda r: r[2]) if sort_by == "cost" else (lambda r: r[1])
        rows.sort(key=key_fn, reverse=desc)

        for r in rows:
            mpe = r[0].model
            if getattr(r[0], "effort", None) and (
                r[0].model.startswith("o") or r[0].model.startswith("gpt-5")
            ):
                mpe = f"{r[0].model}.{r[0].effort}"

            dur_str = f"{r[0].duration:.1f}s" if r[0].duration is not None else "-"

            table.add_row(
                r[0].local_time(),
                mpe,
                f"{r[0].input:,}",
                f"{r[0].output:,}",
                f"{r[0].cached:,}",
                f"${self._cost(r[0].model, r[0])[3]:.6f}",
                f"${r[3]:.6f}",
                dur_str,
                r[0].service_tier,
                r[0].notes or "-",
            )

        # Calculate parallelism metrics
        metrics = self.calculate_parallelism_metrics()
        wall_clock = metrics["wall_clock_time"]

        # Update footers with totals
        table.columns[2].footer = f"{tot_in:,}"
        table.columns[3].footer = f"{tot_out:,}"
        table.columns[4].footer = f"{tot_cache:,}"
        table.columns[5].footer = f"${tot_cost:.6f}"
        table.columns[6].footer = f"${tot_saved:.6f}"

        # Show both wall-clock and compute time in footer
        if tot_duration > 0:
            if wall_clock > 0 and wall_clock < tot_duration:
                # Parallel processing detected
                table.columns[7].footer = f"W:{wall_clock:.1f}s C:{tot_duration:.1f}s"
            else:
                # Sequential or no parallelism detected
                table.columns[7].footer = f"{tot_duration:.1f}s"
        else:
            table.columns[7].footer = ""

        if console:
            console.print(table)
            return self.report_detail(sort_by=sort_by, desc=desc)  # Return text version
        return table

    def report_parallelism(self) -> str:
        """Return a detailed report of parallelism metrics."""
        metrics = self.calculate_parallelism_metrics()

        lines = []
        lines.append("=" * 60)
        lines.append("PARALLELISM METRICS")
        lines.append("=" * 60)
        lines.append(f"Wall-clock time:      {metrics['wall_clock_time']:.2f}s")
        lines.append(f"Total compute time:   {metrics['compute_time']:.2f}s")

        if metrics["wall_clock_time"] > 0:
            lines.append(f"Parallelism factor:   {metrics['parallelism_factor']:.2f}x")
            lines.append(
                f"Time saved:           {metrics['compute_time'] - metrics['wall_clock_time']:.2f}s"
            )
            lines.append(f"Overlap percentage:   {metrics['overlap_percentage']:.1f}%")
            lines.append(f"Max concurrent ops:   {metrics['max_concurrent']}")

            efficiency = (
                (metrics["wall_clock_time"] / metrics["compute_time"] * 100)
                if metrics["compute_time"] > 0
                else 100
            )
            lines.append(f"Efficiency:           {efficiency:.1f}%")
        else:
            lines.append("No timing data available")

        lines.append("=" * 60)
        return "\n".join(lines)

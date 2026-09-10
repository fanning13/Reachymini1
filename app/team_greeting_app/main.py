import time
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np

from reachy_mini import ReachyMiniApp
from reachy_mini.utils import create_head_pose


class TeamGreetingApp(ReachyMiniApp):
    """
    Team Greeting App for Reachy Mini.

    Three-stage behavior:
        1. Orient toward an implied user
        2. Greet with head and antennas
        3. Return to neutral
    """

    # ============================================================
    # Named motion / timing parameters
    # Units are included in the variable names and comments.
    # ============================================================

    # Head yaw angle during Stage 1, in degrees.
    ORIENT_HEAD_YAW_DEG = -25.0

    # Duration of Stage 1 orientation motion, in seconds.
    ORIENT_DURATION_S = 3.0

    # Total duration of the greeting behavior, in seconds.
    GREETING_DURATION_S = 4.0

    # Head nod amplitude during greeting, in degrees.
    HEAD_TILT_DEG = 8.0

    # Antenna swing amplitude during greeting, in degrees.
    ANTENNA_SWING_DEG = 15.0

    # Duration of the return-to-neutral motion, in seconds.
    RETURN_DURATION_S = 3.0

    def _log(self, stage: str) -> None:
        """Print a timestamped marker for each stage."""
        timestamp = datetime.now(ZoneInfo("America/New_York")).isoformat(
            timespec="milliseconds"
        )
        print(f"timestamp={timestamp} stage={stage}", flush=True)

    def run(self, reachy_mini, stop_event) -> None:
        """
        Run the three-stage team greeting behavior.

        stop_event is checked between stages and during the
        greeting loop so that the app can stop gracefully.
        """
        try:
            # Stage 1
            self._stage_orient(reachy_mini, stop_event)

            if stop_event.is_set():
                return

            # Stage 2
            self._stage_greet(reachy_mini, stop_event)

            if stop_event.is_set():
                return

            # Stage 3
            self._stage_neutral(reachy_mini, stop_event)

        finally:
            # Always attempt to return the robot to neutral.
            self._go_neutral(reachy_mini)

    # ============================================================
    # Stage 1: Orient
    # ============================================================

    def _stage_orient(self, reachy_mini, stop_event) -> None:
        self._log("orient")

        if stop_event.is_set():
            return

        # Turn the head toward an implied user.
        orient_pose = create_head_pose(
            roll=0.0,
            pitch=0.0,
            yaw=self.ORIENT_HEAD_YAW_DEG,
            degrees=True,
            mm=True,
        )

        reachy_mini.goto_target(
            head=orient_pose,
            antennas=[0.0, 0.0],
            duration=self.ORIENT_DURATION_S,
        )

        self._interruptible_wait(stop_event, 0.2)

    # ============================================================
    # Stage 2: Greet
    # ============================================================

    def _stage_greet(self, reachy_mini, stop_event) -> None:
        self._log("greet")

        start = time.time()

        # Duration of each half-cycle, in seconds.
        step_duration_s = 0.3

        going_up = True

        while (time.time() - start) < self.GREETING_DURATION_S:

            # Check for a stop request during the loop.
            if stop_event.is_set():
                return

            sign = 1.0 if going_up else -1.0

            # Head nod.
            nod_pose = create_head_pose(
                roll=0.0,
                pitch=sign * self.HEAD_TILT_DEG,
                yaw=self.ORIENT_HEAD_YAW_DEG,
                degrees=True,
                mm=True,
            )

            # Antenna API expects radians.
            antenna_rad = np.deg2rad(
                sign * self.ANTENNA_SWING_DEG
            )

            reachy_mini.goto_target(
                head=nod_pose,
                antennas=[antenna_rad, antenna_rad],
                duration=step_duration_s,
            )

            going_up = not going_up

            # Check stop_event again after each motion.
            if self._interruptible_wait(stop_event, 0.0):
                return

    # ============================================================
    # Stage 3: Return to neutral
    # ============================================================

    def _stage_neutral(self, reachy_mini, stop_event) -> None:
        self._log("neutral")

        self._go_neutral(reachy_mini)

        self._interruptible_wait(stop_event, 0.5)

    # ============================================================
    # Helper functions
    # ============================================================

    def _go_neutral(self, reachy_mini) -> None:
        """Return head and antennas to neutral."""
        neutral_pose = create_head_pose(
            roll=0.0,
            pitch=0.0,
            yaw=0.0,
            degrees=True,
            mm=True,
        )

        reachy_mini.goto_target(
            head=neutral_pose,
            antennas=[0.0, 0.0],
            duration=self.RETURN_DURATION_S,
        )

    def _interruptible_wait(
        self,
        stop_event,
        seconds: float,
    ) -> bool:
        """
        Wait for a short period.

        Returns True immediately if stop_event is triggered.
        """
        return stop_event.wait(timeout=seconds)
if __name__ == "__main__":
    TeamGreetingApp().wrapped_run()
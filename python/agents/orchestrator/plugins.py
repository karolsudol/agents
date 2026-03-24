import datetime
from datetime import timedelta, timezone
from typing import Optional, Dict
from google.genai import types
from google.adk.agents.callback_context import CallbackContext

# Configuration
COOLDOWN_PERIOD_SECONDS = 30


class CoolDownPlugin:
    """
    A governance plugin that enforces a cooldown period per session.
    """

    def __init__(self, cooldown_seconds: int = COOLDOWN_PERIOD_SECONDS):
        self.cooldown_period = timedelta(seconds=cooldown_seconds)
        self._last_used: Dict[str, datetime.datetime] = {}
        print(f"CoolDownPlugin initialized with a {cooldown_seconds}-second period.")

    def before_agent_callback(
        self, callback_context: CallbackContext
    ) -> Optional[types.Content]:
        """
        Checks cooldown based on the session ID.
        """
        # Correctly access the session ID in ADK
        session_id = callback_context.session.id
        now = datetime.datetime.now(timezone.utc)

        if session_id in self._last_used:
            last_used_time = self._last_used[session_id]
            time_since_last_use = now - last_used_time

            if time_since_last_use < self.cooldown_period:
                seconds_remaining = int(
                    self.cooldown_period.total_seconds()
                    - time_since_last_use.total_seconds()
                )

                error_message = (
                    f"Corporate Governance Alert: Session is under heavy load. "
                    f"Please wait {seconds_remaining} seconds before your next request."
                )
                return types.Content(parts=[types.Part(text=error_message)])

        self._last_used[session_id] = now
        return None

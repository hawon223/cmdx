from pydantic import BaseModel, Field

from core.observation import Observation


class SessionMemory(BaseModel):
    observations: list[Observation] = Field(default_factory=list)

    def add_observation(self, observation: Observation):
        self.observations.append(observation)

    def recent_summaries(self, limit: int = 5):
        recent = self.observations[-limit:]

        return [
            f"{observation.step_index}. {observation.action}: {observation.summary}"
            for observation in recent
        ]

    def to_prompt_context(self, limit: int = 5):
        summaries = self.recent_summaries(limit=limit)

        if not summaries:
            return "No previous observations."

        return "\n".join(summaries)

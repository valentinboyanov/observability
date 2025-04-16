import sys
import unittest

from project_spec import N, Proj

proj = Proj(
    [
        N(
            "valentin_is_better_at_infra",
            ["@valentyinboyanov"],
            "@valentinboyanov has a better understanding of his level in infrastructure and is more confident in what he knows and can do.",
            ["observability_solution_ready"],
        ),
        N(
            "observability_solution_ready",
            ["@valentyinboyanov"],
            "The observatility solution is ready to be used by a small product team in production environment.",
            ["ivan_approved", "production_deploy"],
        ),
        N(
            "ivan_approved",
            ["@igarridot"],
            "@igarridot has reviewed and confirmed that the solution is suitable for the purpose of this learning exercise.",
        ),
        N(
            "production_deploy",
            ["@valentyinboyanov"],
            "The solution can be deployed on production environment.",
            ["min_working_solution"],
        ),
        N(
            "min_working_solution",
            ["@valentyinboyanov"],
            "A minimal working solution using the selected tools can be run locally.",
            ["research_done"],
        ),
        N(
            "research_done",
            ["@valentyinboyanov"],
            "Research on the state of the art in observability is complete.",
            ["scope_defined", "basic_concepts_learned"],
        ),
        N(
            "basic_concepts_learned",
            ["@valentyinboyanov"],
            "@valentyinboyanov has learned the fundamental ideas: monitoring (metrics, logs, traces) and observability (understanding system behavior).",
            ["current_level_assessed"],
        ),
        N(
            "scope_defined",
            ["@valentyinboyanov", "@igarridot"],
            "We have explicitly defined the expected usage, limitations, and what constitutes a 'small' product team.",
            ["current_level_assessed"],
        ),
        N(
            "current_level_assessed",
            ["@valentyinboyanov", "@igarridot"],
            "@valentyinboyanov's current level at infra is assessed using the 'knowledge ladder' framework.",
        ),
    ],
    rankdir="TB",
)


class Test(unittest.TestCase):
    def test(self):
        print(proj.to_gv())
        print(proj.to_table())


if __name__ == "__main__":
    command = sys.argv[1]

    if command == "gv":
        print(proj.to_gv())
    elif command == "table":
        print(proj.to_table())
    else:
        raise Exception("unknown command {0}".format(command))

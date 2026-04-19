# -*- coding: utf-8 -*-
"""Pipeline manual: deploy-motd-local (teste echo + hosts do inventário)."""

from __future__ import annotations

from buildbot.plugins import schedulers, steps, util

from devops.ansible.inventory.utils import ansible_json_inventory_targets


class RefreshingInventoryChoiceParameter(util.ChoiceStringParameter):
    """
    Opções lidas de hosts.json em cada pedido da UI (getSpec), sem buildbot reconfig.

    O ChoiceStringParameter normal fixa `choices` na criação do scheduler; aqui
    `choices` é uma propriedade que volta a ler o inventário.
    """

    def __init__(
        self,
        name: str,
        label: str | None = None,
        *,
        inventory_field: str,
        **kwargs,
    ):
        self._inventory_field = inventory_field
        kwargs.pop("choices", None)
        super().__init__(name, label, **kwargs)

    @property
    def choices(self):
        groups, hosts = ansible_json_inventory_targets()
        if self._inventory_field == "group":
            return [""] + list(groups)
        return ["127.0.0.1"] + [h for h in hosts if h != "127.0.0.1"]


def add_deploy_motd(c, worker_name: str) -> None:
    """Acrescenta scheduler Force + builder deploy-motd-local a `c`.

    Nome explícito para evitar colisão com qualquer ``register`` noutros imports.
    As listas vêm de ``RefreshingInventoryChoiceParameter``.
    """
    c["schedulers"].append(
        schedulers.ForceScheduler(
            name="deploy-motd-local",
            builderNames=["deploy-motd-local"],
            buttonName="deploy",
            reason=util.StringParameter(
                name="reason",
                default="deploy manual",
                hide=True,
            ),
            priority=util.IntParameter(
                name="priority",
                default=0,
                hide=True,
            ),
            codebases=[
                util.CodebaseParameter(
                    codebase="",
                    hide=True,
                    branch=None,
                    revision=None,
                    repository=None,
                    project=None,
                )
            ],
            properties=[
                RefreshingInventoryChoiceParameter(
                    name="target_group",
                    label="Grupo alvo",
                    inventory_field="group",
                    default="",
                    strict=True,
                ),
                RefreshingInventoryChoiceParameter(
                    name="target_host",
                    label="Host alvo",
                    inventory_field="host",
                    default="127.0.0.1",
                    strict=True,
                ),
            ],
        )
    )

    factory = util.BuildFactory()
    factory.addStep(
        steps.ShellCommand(
            name="deploy-motd-local",
            command=[
                "bash",
                "-lc",
                util.Interpolate(
                    "echo 'Deploy de teste para host=%(prop:target_host)s grupo=%(prop:target_group)s via Buildbot em '$(date) "
                    "| tee /tmp/buildbot-motd.txt"
                ),
            ],
        )
    )

    c["builders"].append(
        util.BuilderConfig(
            name="deploy-motd-local",
            workernames=[worker_name],
            factory=factory,
        )
    )


register = add_deploy_motd

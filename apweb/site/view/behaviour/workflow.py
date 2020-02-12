# -*- coding:utf-8 -*-
from apweb.utils import context_reify


class WorkflowBehaviour(object):

    workflow_state = context_reify("workflow_state", reify=True)

    @reify
    def workflow_transitions(self):
        return getattr(self.context, "workflow_transitions", None)

    @reify
    def has_workflow(self):
        return self.workflow_transitions is not None

    @reify
    def workflow_actions(self):
        if self.has_workflow:
            actions = []
            for action, transition in self.workflow_transitions.items():
                if self.workflow_state in transition["from"]:
                    actions.append(action)
            return actions
        return []
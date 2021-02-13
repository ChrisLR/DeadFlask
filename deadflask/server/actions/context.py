class ContextAction(object):
    name = ""
    requires_select_target = False
    requires_select_item = False
    requires_freeform_text = False

    @classmethod
    def can_execute(cls, character) -> bool:
        """
        This method is used to define if a character could use the action.
        No targets are passed at this point
        :param character: The character executing the action
        :type character: deadflask.server.models.characters.Character

        :return: Whether the action could be executed or not
        :rtype: bool
        """
        return True

    @classmethod
    def execute(cls, character, target=None, item=None, text=None):
        """
        This method executes the action if possible and returns if the action was executed.
        As long as the action is executed it should return True, even if it failed (ex: A missed attack)
        :param character: The character executing the action
        :type character: deadflask.server.models.characters.Character
        :param target: The selected target character on the receiving end
        :type target: deadflask.server.models.characters.Character
        :param item:  The selected item used in the action
        :param text:  The freeform text if any

        :return: Whether the action was executed or not
        :rtype: bool
        """
        return True

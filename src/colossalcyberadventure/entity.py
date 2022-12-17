import arcade


class IEntity:
    def draw(self, window: arcade.Window):
        """ Draws the entity on the screen

        Parameters
        ----------
        window: arcade.Window
            The window you want to draw the entity on

        Raises
        ------
        NotImplementedError
            If the method is not overriden

        Returns
        -------

        """
        raise NotImplementedError("draw() method not implemented")

    def update(self):
        """

        Raises
        ------
        NotImplementedError
            If the method is not overriden

        Returns
        -------

        """
        raise NotImplementedError("update() method not implemented")

    def get_position(self):
        """Returns entity position

        Raises
        ------
        NotImplementedError
            If the method is not overriden

        Returns
        -------

        """
        raise NotImplementedError("get_position() method not implemented")

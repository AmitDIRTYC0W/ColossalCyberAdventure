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
            If the method is not overrided

        Returns
        -------
        None
        """
        raise NotImplementedError("draw() method not implemented")

    def update(self):
        """

        Raises
        ------
        NotImplementedError
            If the method is not overrided

        Returns
        -------
        None
        """
        raise NotImplementedError("update() method not implemented")

    def getX(self) -> int:
        """

        Raises
        ------
        NotImplementedError
            If the method is not overrided

        Returns
        -------
        int
            player x
        """
        raise NotImplementedError("getX() method not implemented")

    def getY(self):
        """

        Raises
        ------
        NotImplementedError
            If the method is not overrided

        Returns
        -------
        int
            player y
        """
        raise NotImplementedError("getY() method not implemented")

# Create a BoxLayout at the bottom with horizontal alignment
        bottom_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50, padding=[10, 5])

        # List to hold rectangles for later adjustment
        rects_to_update = []

        # Add rectangles to the BoxLayout
        for i in range(4):
            rect_widget = Widget()
            with rect_widget.canvas:
                Color(0, 1, 0, 1)  # Green color
                rect = Rectangle(size=(25, 25))
                rects_to_update.append((rect, rect_widget))
            bottom_layout.add_widget(rect_widget)

        popup_content.add_widget(bottom_layout)
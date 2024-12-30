import sys
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from XMLGRAPH import parse_xml_to_graph, visualize_graph

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout,
    QPushButton, QWidget, QLabel, QHBoxLayout, QMessageBox, QInputDialog
)

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from CONSISTENCY import fix_xml_consistency, check_xml_consistency
from CONVERT_TO_JSON import xml_to_json
from MINIFYING import minify_xml
from COMPRESSION import compress_xml_content  # Import the compress_xml function from the updated compression file
from DECOMPRESSION import decompress_xml_content  
from FORMATTING import formatting 
from NETWORK_ANALYSIS import *
from POST_SEARCH import *



class XMLApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph_canvas = None
        self.setWindowTitle("XML File Processor")
        self.setGeometry(100, 100, 800, 600)

        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QPushButton {
                background-color: #5e2778; /* Dark Purple */
                color: white;
                border: 1px solid #402044;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #7e399c; /* Lighter Purple on Hover */
            }
            QTextEdit {
                background-color: #3c3f41;
                color: #f0f0f0;
                border: 1px solid #555555;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                color: #ffffff;
                font-weight: bold;
                margin: 5px 0;
            }
            QMessageBox {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555555;
            }
            QInputDialog {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555555;
            }
        """)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Input Area
        self.layout.addWidget(QLabel("Input XML:"))
        self.input_text = QTextEdit()
        self.layout.addWidget(self.input_text)

        # Buttons Layout
        self.button_layout_1 = QHBoxLayout()
        self.button_layout_2 = QHBoxLayout()

        # Adding Buttons
        self.add_buttons()

        # Output Area
        self.layout.addWidget(QLabel("Output:"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Graph Visualization
        self.layout.addWidget(QLabel("Graph Visualization:"))
        self.graph_widget = QWidget()
        self.layout.addWidget(self.graph_widget)

        # Show welcome message
        self.show_welcome_message()

    def add_buttons(self):
        # First row of buttons
        buttons_row_1 = [
            ("Load XML File", self.load_xml_file),
            ("Save Output", self.save_output),
            ("Check Consistency", self.check_consistency),
            ("Fix Consistency", self.fix_consistency),
            ("Convert to JSON", self.convert_to_json),
            ("Minify XML", self.minify_xml_content),
            ("Compress XML", self.compress_xml),
            ("Decompress XML", self.decompress_xml),
            ("Format XML", self.format_xml_content),
        ]

        for text, method in buttons_row_1:
            button = QPushButton(text)
            button.clicked.connect(method)
            self.button_layout_1.addWidget(button)

        self.layout.addLayout(self.button_layout_1)

        # Second row of buttons
        buttons_row_2 = [
            ("Visualize Graph", self.display_graph),
            ("Save Graph", self.save_graph),
            ("Most Influential User", self.most_influencer),
            ("Most Active User", self.most_active_user),
            ("Mutual Followers", self.mutual_followers),
            ("Suggest Users", self.suggest_users),
            ("Word Search", self.word_search),
            ("Topic Search", self.topic_search),
        ]

        for text, method in buttons_row_2:
            button = QPushButton(text)
            button.clicked.connect(method)
            self.button_layout_2.addWidget(button)

        self.layout.addLayout(self.button_layout_2)

    def show_welcome_message(self):
        """Show a welcome message when the app starts."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Welcome!")
        msg_box.setText("Welcome to Our XML Editor Program!!!")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555555;
            }
            QPushButton {
                background-color: #5e2778;
                color: white;
                border: 1px solid #402044;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7e399c;
            }
        """)
        msg_box.exec_()

    def load_xml_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml);;All Files (*)")
        if file_name:
            self.clear_graph_display()  
            self.output_text.clear()
            with open(file_name, "r", encoding="utf-8") as file:
                self.input_text.setText(file.read())
            self.loaded_file = file_name    

    def save_output(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Output File", "", "JSON Files (*.json);;XML Files (*.xml);;All Files (*)")
        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(self.output_text.toPlainText())

    def check_consistency(self):
        self.clear_graph_display()  
        self.output_text.clear()
        input_xml = self.input_text.toPlainText().splitlines()
        if input_xml:
            is_valid, errors = check_xml_consistency(input_xml)
            if is_valid:
                self.clear_graph_display()
                QMessageBox.information(self, "Consistency Check", "The XML file is valid and consistent.")
            else:
                error_message = "\n".join([f"Line {line}: {msg}" for line, msg in errors])
                QMessageBox.warning(self, "Consistency Errors", f"The XML file has errors:\n\n{error_message}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

    def fix_consistency(self):
        self.clear_graph_display()
        self.output_text.clear()
        input_xml = self.input_text.toPlainText().splitlines()
        if input_xml:
            is_valid, errors = check_xml_consistency(input_xml)
            if not is_valid:
                fixed_lines, error_log = fix_xml_consistency(input_xml, errors)
                self.output_text.setText("\n".join(fixed_lines))
                self.clear_graph_display()
                QMessageBox.information(self, "Fix Consistency", "The errors have been fixed and displayed in the output.")
            else:
                self.clear_graph_display()
                QMessageBox.information(self, "Fix Consistency", "The XML file is already valid. No fixes needed.")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

    def convert_to_json(self):
        self.clear_graph_display()  
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml:
            try:
                json_output = xml_to_json(input_xml)
                self.output_text.setText(json_output)
                self.clear_graph_display()
                QMessageBox.information(self, "Conversion Successful", "The XML has been converted to JSON.")
            except ValueError as e:
                QMessageBox.warning(self, "Conversion Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")


    def minify_xml_content(self):
        self.clear_graph_display()  
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()  # Get the input XML
        if input_xml.strip():  # Check if input XML is not empty
            try:
                minified_xml = minify_xml(input_xml)  # Minify the XML
                self.output_text.setText(minified_xml)  # Display the minified XML
                self.clear_graph_display()
                QMessageBox.information(self, "Minify XML", "The XML has been successfully minified.")  
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred while minifying: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")


    def compress_xml(self):
        self.clear_graph_display()  
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():  # Check if input XML is not empty
            try:
                compressed_output = compress_xml_content(input_xml)  # Compress the XML
                self.output_text.setText(compressed_output)  # Display the compressed output
                self.clear_graph_display()
                QMessageBox.information(self, "Compression Successful", "The XML has been successfully compressed.")
            except ValueError as e:
                QMessageBox.warning(self, "Compression Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")



    def decompress_xml(self):
        self.clear_graph_display()  
        self.output_text.clear()
        compressed_data = self.input_text.toPlainText()
        if compressed_data.strip():  # Check if input is not empty
            try:
                decompressed_output = decompress_xml_content(compressed_data)  # Decompress the data
                self.output_text.setText(decompressed_output)  # Display the decompressed XML
                self.clear_graph_display()
                QMessageBox.information(self, "Decompression Successful", "The XML has been successfully decompressed.")
            except ValueError as e:
                QMessageBox.warning(self, "Decompression Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "No compressed data provided!")        
        


        # Define the format_xml_content function
    def format_xml_content(self):
        self.clear_graph_display()  
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():  # Check if input XML is not empty
            try:
                formatted_xml = formatting(input_xml)  # Call the updated formatting function
                self.output_text.setText("\n".join(formatted_xml))
                self.clear_graph_display()
                QMessageBox.information(self, "Formatting Successful", "The XML has been successfully formatted.")
            except ValueError as e:
                QMessageBox.warning(self, "Formatting Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")


    def display_graph(self):
        self.clear_graph_display()  
        self.output_text.clear()
        #if not hasattr(self, "loaded_file"):
        #    QMessageBox.warning(self, "Error", "No XML file loaded! Please load an XML file first.")
        #    return
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():  # Check if input XML is not empty
            try:
                graph, _, _, _, _ = parse_xml_to_graph(input_xml)

                # Visualize the graph and get the matplotlib figure
                self.current_graph_figure = visualize_graph(graph)

                # Remove existing canvas if any
                if self.graph_canvas:
                    self.graph_layout.removeWidget(self.graph_canvas)
                    self.graph_canvas.deleteLater()

                # Add the new graph canvas
                self.graph_canvas = FigureCanvas(self.current_graph_figure)
                # Ensure the graph widget has a layout
                if not self.graph_widget.layout():  # If no layout exists
                    self.graph_widget.setLayout(QVBoxLayout())  # Create a new layout
                    self.graph_widget.layout().addWidget(self.graph_canvas)

                QMessageBox.information(self, "Graph Visualization", "The graph has been visualized successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred during graph visualization: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")        


    def save_graph(self):
        
        if not hasattr(self, "current_graph_figure"):
            QMessageBox.warning(self, "Error", "No graph has been visualized yet! Please visualize the graph first.")
            return

        if self.current_graph_figure:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)")
        if file_name:
            self.current_graph_figure.savefig(file_name)
            QMessageBox.information(self, "Success", f"Graph saved as: {file_name}")
        else:
            QMessageBox.warning(self, "Error", "No graph has been visualized yet! Please visualize the graph first.")



    def clear_graph_display(self):
        try:
            if self.graph_canvas:

                self.graph_canvas.deleteLater()
                self.graph_canvas = None

            # You can also reset the layout to None if necessary
            layout = self.graph_widget.layout()
            widg =self.graph_widget 
            if  widg and layout:
                #layout.clear()  # Clear layout content
                self.graph_widget.setLayout(QVBoxLayout())

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error while clearing the graph: {str(e)}")


    def clear_output_window(self):
        """Clears the output text window."""
        self.output_window.clear()



    def most_influencer(self): 
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():
            try:
                graph, _, _, _, names = parse_xml_to_graph(input_xml)
                influencer_name, influencer_id = most_influencer(graph, names)
                QMessageBox.information(self, "Most Influential User", f"Most Influential User: {influencer_name} (ID: {influencer_id})")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

    def most_active_user(self): 
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():
            try:
                graph, _, _, _, names = parse_xml_to_graph(input_xml)
                active_name, active_id = most_active_user(graph, names)
                QMessageBox.information(self, "Most Active User", f"Most Active User: {active_name} (ID: {active_id})")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

    def mutual_followers(self):
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():
            try:
                graph, _, _, _, _ = parse_xml_to_graph(input_xml)
            
                # Collect user IDs dynamically
                user_ids = []
                while True:
                    user_id, ok = QInputDialog.getText(self, "Mutual Followers", f"Enter User ID {len(user_ids) + 1} (or press Cancel to finish):")

                    if not ok or not user_id:  # User cancels or submits empty input
                        if len(user_ids) < 1:  # Ensure at least two IDs are collected
                            QMessageBox.warning(self, "Error", "At least one User IDs are required!")
                            return
                        break
                
                    if user_id in graph.get_all_nodes():  # Check if the user ID exists in the graph
                        user_ids.append(user_id)
                    else:  # Invalid user ID
                        QMessageBox.warning(self, "Error", f"User ID '{user_id}' does not exist in the given XML!")
                        return
                    
                # Compute mutual followers
                mutual_followers_list = mutual_followers(graph, user_ids)
                if isinstance(mutual_followers_list, str):
                    QMessageBox.information(self, "Mutual Follower ID :", mutual_followers_list)
                else:
                    QMessageBox.information(self, "Mutual Followers", f"Mutual Follower ID : {', '.join(mutual_followers_list)}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

            

    def suggest_users(self):
        self.output_text.clear()
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():
            try:
                graph, _, _, _, _ = parse_xml_to_graph(input_xml)
                # Get the target user ID from the user (you can adjust this to use a dialog box or input field)
                target_user, ok = QInputDialog.getText(self, "Suggest Users", "Enter Target User ID:")
                if ok and target_user in graph.get_all_nodes():
                    suggested_users = suggest_users(graph, target_user)
                    suggestions = "\n".join([f"User ID: {user_id}" for user_id, _ in suggested_users])
                    QMessageBox.information(self, "Suggested Users", f"Suggested Users:\n{suggestions}")
                else:
                    QMessageBox.warning(self, "Error", "Invalid user ID or operation canceled!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

    def word_search(self):
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():
            try:
                # Parse the XML file to get posts data
                graph, posts, _,_, _ = parse_xml_to_graph(input_xml)

                # Ask the user to input the word they want to search for
                word, ok = QInputDialog.getText(self, "Word Search", "Enter the word to search:")
                if ok and word:
                    results = []
                    word = word.lower()
                    for user, user_posts in posts.items():
                        user_posts = [post.lower() for post in user_posts]  # Case-insensitive search
                        for post in user_posts:
                            if word in post:
                                results.append(f"Found '{word}' in post: '{post}' by user: '{user}'")

                    # Display results in the output text area
                    if results:
                        self.output_text.setText("\n".join(results))
                    else:
                        self.output_text.setText(f"'{word}' is not found in any post.")
                else:
                    QMessageBox.warning(self, "Error", "No word entered!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")

    def topic_search(self):
        input_xml = self.input_text.toPlainText()
        if input_xml.strip():
            try:
                # Parse the XML file to get post topics
                graph, _, _,post_topics, _ = parse_xml_to_graph(input_xml)
                print (post_topics)
                # Ask the user to input the topic they want to search for
                topic, ok = QInputDialog.getText(self, "Topic Search", "Enter the topic to search:")
                if ok and topic:
                    results = []
                    for post in post_topics:
                        if topic in post['topics']:
                            results.append(post['body'])

                    # Display results in the output text area
                    if results:
                        self.output_text.setText("\n".join(results))
                    else:
                        self.output_text.setText(f"The topic '{topic}' is not found in any post.")
                else:
                    QMessageBox.warning(self, "Error", "No topic entered!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No input XML provided!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XMLApp()
    window.show()
    sys.exit(app.exec_())

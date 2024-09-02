# Define the source directory
SRC_DIR := posts/universalprior

# Find all .md files in the source directory
MD_FILES := $(wildcard $(SRC_DIR)/*.md)

# Generate the list of target HTML files
HTML_FILES := $(patsubst $(SRC_DIR)/%.md,$(SRC_DIR)/%.html,$(MD_FILES))

# Define the script path
SCRIPT_PATH := index.js
RELATIVESCRIPT_PATH := ../../index.js

# Default target
all: clean_log index.html $(HTML_FILES)

# Clean target
clean:
	rm -f index.html $(HTML_FILES)

# Clean log target
clean_log:
	rm -f sidenote_filter.log

# Rule for index.html
index.html: index.md template.html Makefile
	sed 's|\$$script-path\$$|$(SCRIPT_PATH)|g' template.html > temp_template.html
	pandoc --toc -s --css reset.css --css index.css -i $< -o $@ --template=temp_template.html
	rm temp_template.html

# Rule for other HTML files
$(SRC_DIR)/%.html: $(SRC_DIR)/%.md template.html Makefile
	sed 's|\$$script-path\$$|$(RELATIVESCRIPT_PATH)|g' template.html > temp_template.html
	pandoc --toc -s --css ../../reset.css --css ../../index.css -i $< -o $@ --template=temp_template.html --filter=./sidenote_filter.py
	rm temp_template.html

# Declare phony targets
.PHONY: all clean clean_log
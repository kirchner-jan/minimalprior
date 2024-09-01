# Define the source directory
SRC_DIR := posts/universalprior

# Find all .md files in the source directory
MD_FILES := $(wildcard $(SRC_DIR)/*.md)

# Generate the list of target HTML files
HTML_FILES := $(patsubst $(SRC_DIR)/%.md,$(SRC_DIR)/%.html,$(MD_FILES))

# Default target
all: index.html $(HTML_FILES)

# Clean target
clean:
	rm -f index.html $(HTML_FILES)

# Rule for index.html
index.html: index.md template.html Makefile
	pandoc --toc -s --css reset.css --css index.css -i $< -o $@ --template=template.html

# Rule for other HTML files
$(SRC_DIR)/%.html: $(SRC_DIR)/%.md template.html Makefile
	pandoc --toc -s --css ../../reset.css --css ../../index.css -i $< -o $@ --template=template.html --filter=./sidenote_filter.py

# Declare phony targets
.PHONY: all clean
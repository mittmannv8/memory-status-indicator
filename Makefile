install: install_memory_status_indicator

INSTALL_DIR=~/.config/autostart/
USER=`who -m | cut -d " " -f 1`


install_memory_status_indicator:
	@echo "Copying files to /usr/lib..."
	@cp -r memory_status_indicator /usr/lib
	@if [ ! -d $(INSTALL_DIR) ]; \
	then \
	    echo "Creating $(INSTALL_DIR)... "; \
	    sudo su $(USER) -c "mkdir -p $(INSTALL_DIR)"; \
	fi
	@cp memory_status_indicator.desktop ~/.config/autostart/
	@sudo su $(USER) -c "/usr/lib/memory_status_indicator/memory_status.py 2>&1 /dev/null &"
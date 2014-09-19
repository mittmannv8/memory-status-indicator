install: install_memory_status_indicator


install_memory_status_indicator:
	@echo "Copying files to /usr/lib..."
	cp -r memory_status_indicator /usr/lib
	cp memory_status_indicator.desktop ~/.config/autostart/
	sudo su `who -m | cut -d " " -f 1`  -c "/usr/lib/memory_status_indicator/memory_status.py > /dev/null &"
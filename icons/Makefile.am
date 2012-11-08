app_icons = \
	bookmarks.png

install-data-local:
	@-$(mkinstalldirs) $(datadir)/icons/gnome/32x32/actions
	$(INSTALL_DATA) $(srcdir)/bookmarks.png $(datadir)/icons/gnome/32x32/actions/bookmarks.png

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/gnome/32x32/actions

install-data-hook:
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating Gtk icon cache."; \
		$(gtk_update_icon_cache); \
	else \
		echo "*** Icon cache not updated.  After install, run this:"; \
		echo "***   $(gtk_update_icon_cache)"; \
	fi

uninstall-hook:
	rm -f $(datadir)/icons/gnome/32x32/actions/bookmarks.png
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating Gtk icon cache."; \
		$(gtk_update_icon_cache); \
	else \
		echo "*** Icon cache not updated.  After uninstall, run this:"; \
		echo "***   $(gtk_update_icon_cache)"; \
	fi

update-icon-cache:

EXTRA_DIST = $(app_icons)

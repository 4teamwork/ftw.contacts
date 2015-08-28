$(function() {
    ContactFolderListing.init();
});
var ContactFolderListing = (function($) {

    'use strict';

    var self = {};
    var contactsContainer;
    var loadMoreButton;
    var searchInput;
    var index = 0;
    var step = 20;
    var letter = '';
    var maxContacts = 0;
    var searchableText = '';

    var init = function() {
        contactsContainer = $(
            '#contact-folder-view .contactFolderContactsListig');
        loadMoreButton = $(
            '#contact-folder-view .contactFolderLoadMoreContacts');
        searchInput = $(
            '#contact-folder-view input#contactFolderSearchGadget');

        loadMoreButton.on('click', function(e) {reloadView();});
        $('.contactFolderAlphabeticalSearch .letter').on('click', function(e) {
            letterClick($(this));
        });
        searchInput.on('keyup', function() {
            updateSearch($(this).val());
        });

        reloadView();
    };

    var reloadView = function(reset) {
        reset = typeof reset !== 'undefined' ? reset : false;
        if (reset) {
            index = 0;
        }
        $.getJSON('@@reload', {
                index_from: index,
                index_to: index + step,
                letter: letter,
                searchable_text: searchableText}, function(data) {

            if (reset) {
                contactsContainer.empty();
            }
            // contacts
            contactsContainer.append($(data.contacts));

            index = index + step;
            setMoreButtonVisible(index < data.max_contacts);

            // letters
            $('.contactFolderAlphabeticalSearch').html(data.letters);
            $('.contactFolderAlphabeticalSearch .letter').on('click', function(e) {
                letterClick($(this));
            });
        });
    };

    var letterClick = function(button) {
        var self = $(button);
        if (!self.hasClass('withContent') && !self.hasClass('active')) {
            return;
        }
        // Reset the letter-filter if click on the active letter
        letter = '';
        if (!self.hasClass('active')) {
            letter = self.data('key');
        }
        reloadView(true);
    };

    var setMoreButtonVisible = function(setVisible) {
        if (setVisible) {
            loadMoreButton.show();
        }else {
            loadMoreButton.hide();
        }
    };

    var updateSearch = function(text) {
        searchableText = text;
        reloadView(true);
    };

    self.init = init;
    return self;

}(jQuery));

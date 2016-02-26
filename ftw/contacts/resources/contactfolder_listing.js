var ContactFolderListing = (function($) {

    'use strict';

    var contactsContainer;
    var loadMoreButton;
    var searchInput;
    var index = 0;
    var step = 20;
    var letter = '';
    var maxContacts = 0;
    var searchableText = '';
    var self = this;

    var init = function() {

        contactsContainer = $('#contact-folder-view .contactFolderContactsListig');
        loadMoreButton = $('#contact-folder-view .contactFolderLoadMoreContacts');
        searchInput = $('#contact-folder-view input#contactFolderSearchGadget');

        loadMoreButton.on('click', function(e) {reloadView();});

        $(document).on('click', '.contactFolderAlphabeticalSearch .letter', letterClick);

        searchInput.on('keyup', function() {
            var value = $(this).val();
            delay(function() {
                updateSearch(value);
            }, 200);
        });

        $('input[name=SearchableContactsText]').keypress(disableEnter);

        reloadView();
    };

    var isEnter = function(event) { return event.which === 13; };

    var disableEnter = function(e) {
        if (isEnter(e)) {
            e.preventDefault();
            return false;
        }
    };

    var reloadView = function(reset) {
        reset = typeof reset !== 'undefined' ? reset : false;
        if (reset) {
            index = 0;
        }
        $.getJSON('@@reload_contacts', {
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
            $(document).trigger("contactsReloaded");
        });
    };

    var letterClick = function(e) {
        var letterButton = $(e.currentTarget);
        if (!letterButton.hasClass('withContent') && !letterButton.hasClass('active')) {
            return;
        }
        // Reset the letter-filter if click on the active letter
        letter = '';
        if (!letterButton.hasClass('active')) {
            letter = letterButton.data('key');
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

    var delay = (function() {
        var timer = 0;
        return function(callback, ms) {
            clearTimeout(timer);
            timer = setTimeout(callback, ms);
        };
    })();

    return { init: init };

}(jQuery));

$(ContactFolderListing.init);

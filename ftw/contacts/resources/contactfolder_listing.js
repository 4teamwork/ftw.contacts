$(function() {
    ContactFolderListing.init();
});
var ContactFolderListing = (function($){
    "use strict"
    var self = {};
    var $contactsContainer;
    var $loadMoreButton;
    var $alphabeticalContainer;
    var $searchInput;
    var index = 0;
    var step = 20;
    var letter = '';
    var maxContacts = 0;
    var searchableText = ''

    var init = function(){
        $contactsContainer = $('#contact-folder-view .contactFolderContactsListig');
        $loadMoreButton = $('#contact-folder-view .contactFolderLoadMoreContacts');
        $searchInput = $('#contact-folder-view input#contactFolderSearchGadget');

        $loadMoreButton.on('click', function(e) {reloadView();});
        $('.contactFolderAlphabeticalSearch div.letter').on('click', function(e) { letterClick($(this)); });
        $searchInput.on('keyup', function() {
            updateSearch($(this).val());
        });

        reloadView();
    }
    var reloadView = function() {
        $.getJSON( "@@reload", {
                index_from: index,
                index_to: index + step,
                letter: letter,
                searchable_text: searchableText}, function( data ){

            // contacts
            $contactsContainer.append( $(data.contacts) );

            index = index + step;
            setMoreButtonVisible(index < data.max_contacts);

            // letters
            $('.contactFolderAlphabeticalSearch').html( data.letters );
            $('.contactFolderAlphabeticalSearch div.letter').on('click', function(e) {
                letterClick($(this));
            });
        });
    }
    var letterClick = function(button){
        var $this = $(button);
        if ( !$this.hasClass('withContent') && !$this.hasClass('current')){
            return;
        }
        index = 0;
        $contactsContainer.empty();

        // Reset the letter-filter if click on the current selected letter
        letter = ''
        if ( !$this.hasClass('current') ){
            letter = $this.data('key')
        }
        reloadView();
    }
    var setMoreButtonVisible = function(setVisible){
        if ( setVisible ){
            $loadMoreButton.show();
        }else{
            $loadMoreButton.hide();
        }
    }
    var updateSearch = function(text){
        index = 0;
        $contactsContainer.empty();

        searchableText = text;
        reloadView();
    };
    self.init = init;
    return self
}(jQuery));

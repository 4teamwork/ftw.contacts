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
    var step = 5;
    var letter = '';
    var maxContacts = 0;
    var searchableText = ''

    var init = function(){
        $contactsContainer = $('#contact-folder-view .contactFolderContactsListig');
        $loadMoreButton = $('#contact-folder-view .contactFolderLoadMoreContacts');
        $searchInput = $('#contact-folder-view input#contactFolderSearchGadget');

        $loadMoreButton.on('click', function(e) {loadNextContacts();});
        $('.contactFolderAlphabeticalSearch div.letter').on('click', function(e) { letterClick($(this)); });
        $searchInput.on('keyup', function() {
            updateSearch($(this).val());
        });

        reloadView();
    }
    // var loadNextContacts = function(){
    //     var index_from = index;
    //     var index_to = index + step;

    //     $.getJSON( "@@load_next_contacts", {
    //             index_from: index_from,
    //             index_to: index_to,
    //             letter: letter,
    //             searchable_text: searchableText}, function( data ){

    //         $contactsContainer.append( $(data.html) );
    //         maxContacts = data.max_contacts
    //         index = index + step;

    //         setMoreButtonVisible(index < maxContacts)

    //     });

    // }
    var reloadView = function() {
        $.getJSON( "@@reload", {
                index_from: index,
                index_to: index + step,
                letter: letter,
                searchable_text: searchableText}, function( data ){

            // contacts
            $contactsContainer.empty();
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
        // Reset the letter-filter if click on the current selected letter
        letter = ''
        if ( !$this.hasClass('current') ){
            letter = $this.data('key')
        }
        reloadView();
    }
    // var loadLetters = function(){
    //     $.get( "@@letters", {letter: letter, searchable_text: searchableText}, function( data ){
    //         $('.contactFolderAlphabeticalSearch').html( data );
    //         $('.contactFolderAlphabeticalSearch div.letter').on('click', function(e) {letterClick($(this)); })
    //     });

    // }
    var setMoreButtonVisible = function(setVisible){
        if ( setVisible ){
            $loadMoreButton.show();
        }else{
            $loadMoreButton.hide();
        }
    }
    var updateSearch = function(text){
        index = 0;
        searchableText = text;
        reloadView();
    };
    self.init = init;
    return self
}(jQuery));

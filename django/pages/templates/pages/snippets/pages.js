//
// Cookies
//

// Get a cookie
function cookieGet(name){
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Get a cookie and convert to an array
function cookieGetAsArray(name){
    let cookie = cookieGet(name);
    // If cookie not found, return an empty array
    if (cookie == null) return [];
    // If cookie found return data an array
    else {
        try {
            cookie = JSON.parse(cookie);
            if (Array.isArray(cookie)) return cookie;
            else return [cookie];  // Ensures data is an array
        }
        catch {
            console.error('Error trying to parse cookie as JSON in pages.js. Some features (like My History and My Favourites) may not work properly until this is resolved.');
            return [];
        }
    }
}

// Set (add/edit) a cookie
function cookieSet(name, value){
    document.cookie = `${name}=${value}; expires=Mon, 1 Jan 2080 12:00:00 UTC; path=/`;
}

// Delete a cookie (simply set expiry date in the past)
function cookieDelete(name){
    document.cookie = `${name}=0; expires=Sat, 1 Jan 2000 12:00:00 UTC; path=/`;
}

// Current page details as an object suitable for use in cookies
currentPageObj = {
    'name': '{{ object.name }}'.replace("&#x27;", "'"),
    'slug': '{{ object.meta_slug }}'
}

// If a page object already exists in an array (from a cookie)
function pageExistsInCookieArray(cookieArray, pageObj){
    let pageExists = false;
    cookieArray.forEach(function(page){
        if (JSON.stringify(page) == JSON.stringify(pageObj)) pageExists = true;
    })
    return pageExists;
}


//
// Media Files and Links
//

// Function to load content into a particular media viewer (e.g. audio or video) and display it
function mediaViewerLoad(media_type, media_url, media_file_type){
    $(`#pages-mediaviewer`).html('').append(
        `<div class="pages-mediaviewer-close"><i class="fas fa-times-circle"></i></div>
        <${media_type} controls><source src="${media_url}" type="${media_type}/${media_file_type}"></${media_type}>`
    ).addClass('active').find(media_type)[0].play();
}

// Customise behaviour when clicking on <a> tags (e.g. load media or simply follow link)
$('a').on('click', function(e){
    // Stop default behaviour of links (e.g. downloading file or going to the new page)
    e.preventDefault();
    // Determine URL and file type of linked resource
    url = $(this).attr('href');
    url_file_type = (typeof url !== 'undefined' ? url.split('.').at(-1).toLowerCase() : false);
    // Audio player
    if (['wav', 'mp3'].includes(url_file_type)) mediaViewerLoad('audio', url, url_file_type);
    // Video player
    else if (url_file_type === 'mp4') mediaViewerLoad('video', url, url_file_type);
    // PDFs
    else if (url_file_type == 'pdf') window.open(url, '_blank');
    // For all other links (with a valid url file type) simply go to URL in current window
    else if (url_file_type) window.open(url, '_parent');
});

// Close the current media viewer
$('body').on('click', '.pages-mediaviewer-close', function(){
    // Remove active class, which will animate the media viewer closing via CSS
    $('#pages-mediaviewer').removeClass('active');
    // Once animation has finished, empty content of the viewer to end media playback
    setTimeout(function(){ $('#pages-mediaviewer').html(''); }, 100);
});


//
// Accordions
//

// Expand function
function accordionExpand(accordionHead){
    if($(accordionHead).next().is(":hidden")){
        $(accordionHead).next().slideDown();
        $(accordionHead).find('.accordion-head-symbol').html('<i class="fas fa-minus"></i>');
    } else return false;
}

// Collapse function
function accordionCollapse(accordionHead){
    if($(accordionHead).next().is(":visible")){
        $(accordionHead).next().slideUp();
        $(accordionHead).find('.accordion-head-symbol').html('<i class="fas fa-plus"></i>');
    } else return false;
}

// Toggle event
$('.accordion-head').on('click', function() {
    if(accordionExpand(this) === false) accordionCollapse(this);
});

// Expand all event
$('.accordion-all-expand').on('click', function() {
    $('.accordion-head').each(function(){ accordionExpand(this); });
});

// Collapse all event
$('.accordion-all-collapse').on('click', function() {
    $('.accordion-head').each(function(){ accordionCollapse(this); });
}).trigger('click');

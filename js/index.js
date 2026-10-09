
$(document).ready(function () {
    // Add smooth scrolling to all links
    $("a").on('click', function (event) {

        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();

            // Store hash
            var hash = this.hash;

            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (500) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
                scrollTop: $(hash).offset().top - 70
            }, 500, function () {

                // // Add hash (#) to URL when done scrolling (default click behavior)
                // window.location.hash = hash;
            });
        } // End if 
    });
});

$(document).ready(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
        $('.navbar').toggleClass('scrolled', $(this).scrollTop() > 10);
    });
    
    // scroll body to 0px on click
    $('#back-to-top').click(function () {
        // $('#back-to-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    // $('#back-to-top').tooltip('show');
});

// Fade blocks up as they scroll into view (styles in css/style.css under "Scroll reveal").
// Only blocks still below the fold are hidden, so nothing visible on load flickers.
$(document).ready(function () {
    if (!('IntersectionObserver' in window) ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.filter(function (entry) { return entry.isIntersecting; })
            .forEach(function (entry, i) {
                // stagger blocks that arrive together
                entry.target.style.setProperty('--reveal-delay', (i * 0.08) + 's');
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
    }, { rootMargin: '0px 0px -40px 0px' });

    $('.section-title, .my-education > li, .timeline > li, #publications ol, .achievements, #project-div > div')
        .each(function () {
            if (this.getBoundingClientRect().top > window.innerHeight) {
                this.classList.add('reveal');
                observer.observe(this);
            }
        });
});


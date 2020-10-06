var currentSlide = 0,
    $slideContainer = $('.slide-container'),
    $slide = $('.slide'),
    slideCount = $slide.length,
    animationTime = 300;

function setSlideDimensions() {
    var windowWidth = $(window).width();
    $slideContainer.width(windowWidth * slideCount);
    $slide.width(windowWidth);
}

function generatePagination() {
    var $pagination = $('.pagination');
    for (var i = 0; i < slideCount; i++) {
        var $indicator = $('<div>').addClass('indicator'),
            $progressBarContainer = $('<div>').addClass('progress-bar-container'),
            $progressBar = $('<div>').addClass('progress-bar'),
            indicatorTagText = $slide.eq(i).attr('data-tag'),
            $tag = $('<div>').addClass('tag').text(indicatorTagText);
        $indicator.append($tag);
        $progressBarContainer.append($progressBar);
        $pagination.append($indicator).append($progressBarContainer);
    }
    $pagination.find('.indicator').eq(0).addClass('active');
}

function goToNextSlide() {
    if (currentSlide >= slideCount - 1) return;
    var windowWidth = $(window).width();
    currentSlide++;
    $slideContainer.animate({
        left: -(windowWidth * currentSlide)
    });
    setActiveIndicator();
    $('.progress-bar').eq(currentSlide - 1).animate({
        width: '100%'
    }, animationTime);
}

function goToPreviousSlide() {
    if (currentSlide <= 0) return;
    var windowWidth = $(window).width();
    currentSlide--;
    $slideContainer.animate({
        left: -(windowWidth * currentSlide)
    }, animationTime);
    setActiveIndicator();
    $('.progress-bar').eq(currentSlide).animate({
        width: '0%'
    }, animationTime);
}

function postitionSlides() {
    var windowWidth = $(window).width();
    setSlideDimensions();
    $slideContainer.css({
        left: -(windowWidth * currentSlide)
    }, animationTime);
}

function setActiveIndicator() {
    var $indicator = $('.indicator');
    $indicator.removeClass('active').removeClass('complete');
    $indicator.eq(currentSlide).addClass('active');
    for (var i = 0; i < currentSlide; i++) {
        $indicator.eq(i).addClass('complete');
    }
}

setSlideDimensions();
generatePagination();
$(window).resize(postitionSlides);
$('.next').on('click', goToNextSlide);
$('.previous').on('click', goToPreviousSlide);


$('.ui.rating')
    .rating({
        initialRating: 3,
        maxRating: 5
    });
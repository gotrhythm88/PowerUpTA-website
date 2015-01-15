/* Javascript for scratch card */

$('#i-info-scratch').click(function()
{
	/* icons */
	$('#i-info-scratch').css('display','none');
	$('#i-close-scratch').show();
	$('#i-scratch').show();
	
	/* content */
	$('#accordion-scratch').css('display','none');
	$('#desc-scratch').show();

	/* color */
	$('#card-scratch').css('background','#bbd4de');	
});


$('#i-close-scratch').click(function()
{
	/* icons */
	$('#i-info-scratch').show();
	$('#i-close-scratch').css('display','none');
	$('#i-scratch').css('display','none');
	
	/* content */
	$('#accordion-scratch').show();
	$('#desc-scratch').css('display','none');

	/* color */
	$('#card-scratch').css('background','#e4eef2');	

});

/* Javascript for scratchjr card */

$('#i-info-scratchjr').click(function()
{
	/* icons */
	$('#i-info-scratchjr').css('display','none');
	$('#i-close-scratchjr').show();
	$('#i-scratchjr').show();
	
	/* content */
	$('#accordion-scratchjr').css('display','none');
	$('#desc-scratchjr').show();

	/* color */
	$('#card-scratchjr').css('background','#bbd4de');	
});


$('#i-close-scratchjr').click(function()
{
	/* icons */
	$('#i-info-scratchjr').show();
	$('#i-close-scratchjr').css('display','none');
	$('#i-scratchjr').css('display','none');
	
	/* content */
	$('#accordion-scratchjr').show();
	$('#desc-scratchjr').css('display','none');

	/* color */
	$('#card-scratchjr').css('background','#e4eef2');	

});

/* Javascript for website card */

$('#i-info-website').click(function()
{
	/* icons */
	$('#i-info-website').css('display','none');
	$('#i-close-website').show();
	$('#i-website').show();
	
	/* content */
	$('#accordion-website').css('display','none');
	$('#desc-website').show();

	/* color */
	$('#card-website').css('background','#bbd4de');	
});


$('#i-close-website').click(function()
{
	/* icons */
	$('#i-info-website').show();
	$('#i-close-website').css('display','none');
	$('#i-website').css('display','none');
	
	/* content */
	$('#accordion-website').show();
	$('#desc-website').css('display','none');

	/* color */
	$('#card-website').css('background','#e4eef2');	

});


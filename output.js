/* Javascript */

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
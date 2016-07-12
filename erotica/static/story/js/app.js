console.log("hello world")



pickBranch = $('#pick-branch')//document.getElementById('pick-branch')
if (pickBranch) {
	pickBranch.click(function() {
		links = $('.branch-link')//document.getElementsByClassName('branch-link')
		numBranches = links.length
		rand = Math.floor(Math.random() * (numBranches))
		scrollThroughLinks(300)

	  });
}

function scrollThroughLinks(time, linkNum){
	
		numBranches = links.length
		
		rand = Math.floor(Math.random() * (numBranches))
		while(linkNum == rand){
			rand = Math.floor(Math.random() * (numBranches))
		}
		selector = ".branch-link:eq("+rand+")"
		$(selector).addClass('hover')


		setTimeout(function(){

			if (time >=1400){
				return $(selector)[0].click()
			} else {
				$(selector).removeClass('hover')
				time*=1.15
				scrollThroughLinks(time, rand)
			}
		}, time)
}
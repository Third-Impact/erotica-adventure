console.log("hello world")



pickBranch = $('#pick-branch')//document.getElementById('pick-branch')
if (pickBranch) {
	pickBranch.click(function() {
		links = $('.branch-link')//document.getElementsByClassName('branch-link')
		numBranches = links.length
		rand = Math.floor(Math.random() * (numBranches))
		dieSim = dieSimulator(links)
		scrollThroughLinks(dieSim)
	  });
}

function scrollThroughLinks(die){
	
		// numBranches = links.length
		
		// rand = Math.floor(Math.random() * (numBranches))
		// while(linkNum == rand){
		// 	rand = Math.floor(Math.random() * (numBranches))
		// }
		// selector = ".branch-link:eq("+rand+")"

		// el = $(selector)

		die.animation()

		setTimeout(function(){
			die.next()
			if (die.time() >= 1000){
				die.animationEnlarge()
				return

			} else {
				scrollThroughLinks(die)
			}

		}, die.time())
}



var dieSimulator = function(links){

	var time=400
	var element = select()
	var numBranches = links.length
	var linkNum = rand = Math.floor(Math.random() * (numBranches))

	function incTime(){
		time*=1.15
	}

	function select(){
		while(linkNum == rand){
			rand = Math.floor(Math.random() * (numBranches))
		}
		linkNum = rand
		selector = ".branch-link:eq("+linkNum+")"
		return $(selector)
	}

	return {
		animation: function (){
			element.animate({
				letterSpacing:"2px"
						// color: "black"
			}, time/2.5,  function(){
				element.animate({
					letterSpacing: "-=2" 
				}, time/2.5)
			})
		},

		animationEnlarge: function(){
			element.animate({
				letterSpacing:"2px"
			}, time, function(){
				return element[0].click()
			})
		},

		time: function(){
			return time
		},

		next: function(){
		
			element = select()

			incTime()
		}
	}

}
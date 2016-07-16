console.log("app.js loaded")


pickBranch = $('#pick-branch')//document.getElementById('pick-branch')
if (pickBranch) {
	pickBranch.click(function() {
		links = $('.branch-link')//document.getElementsByClassName('branch-link')

		dieSim = new DieSimulator(links)
		// scrollThroughLinks(dieSim)
		dieSim.roll()
	  });
}


var DieSimulator = function(links){

	this.time=400
	this.numBranches = links.length
	this.linkNum = this.rand = Math.floor(Math.random() * (this.numBranches))
	this.selectNext()
}

// randomly pick the next link
DieSimulator.prototype.selectNext = function(){
		// this.rand = Math.floor(Math.random() * (numBranches))
	while(this.linkNum == this.rand){
		this.rand = Math.floor(Math.random() * (this.numBranches))
	}
	this.linkNum = this.rand
	selector = ".branch-link:eq("+this.linkNum+")"
	this.element = $(selector)
		// return $(selector)
}

// enlarge and shrink the selected link
DieSimulator.prototype.animation = function (){
		// this.element = this.select()
	el = this.element
	time= this.time
	var startingColor = el.css("color")
	console.log(startingColor)
	// el.css({"outline": "2px solid"})
	// el.css("color", "red")
	el.animate({
		letterSpacing:"2px"
						// color: "black"
	}, time/2.5,  function(){
		el.animate({
			letterSpacing: "-=2" 
		}, time/2.5, function(){
			// $(this).css("color", startingColor)
		})
	})
}

// enlarges and follows the last selection as if it were clicked.
DieSimulator.prototype.animationEnlarge = function(){
	el = this.element
	time = this.time
	// el.css({"outline": "2px solid"})
	el.css({"color": "red"})
	el.animate({
		letterSpacing:"2px"
	}, time, function(){
		return el[0].click()
	})
}

// pick the next link element and slow down the roll time
// DieSimulator.prototype.next = function(){
// 			// this.element = this.select()
// 	this.selectNext()
// 	// this.incTime()
// 	this.time*=1.15
// }

// recursive roll function which randomly selects branch links.
DieSimulator.prototype.roll = function(){
	this.animation()
	// setTimeout(this.rollFunc, time)
	setTimeout( (function(){
		// this.next()
		this.selectNext()
		this.time*=1.15
		if (this.time >= 1000){
			this.animationEnlarge()
			return
		} else {
			this.roll()
		}

	}).bind(this), this.time )
}

// DieSimulator.prototype.rollFunc = function(){
// 	// this.next()
// 		this.selectNext()
// 		this.time*=1.15
// 	if (this.time >= 1000){
// 		this.animationEnlarge()
// 		return
// 	} else {
// 		this.roll()
// 	}
// }
	


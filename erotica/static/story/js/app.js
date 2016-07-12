console.log("hello world")



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
	this.element = this.select()
}

DieSimulator.prototype.incTime = function(){
	this.time*=1.15
}

DieSimulator.prototype.select = function(){
		// this.rand = Math.floor(Math.random() * (numBranches))
		while(this.linkNum == this.rand){
			this.rand = Math.floor(Math.random() * (this.numBranches))
		}
		this.linkNum = this.rand
		selector = ".branch-link:eq("+this.linkNum+")"
		return $(selector)
}

	// return {
DieSimulator.prototype.animation = function (){
		// this.element = this.select()
		el = this.element
		time= this.time
			el.animate({
				letterSpacing:"2px"
						// color: "black"
			}, time/2.5,  function(){
				el.animate({
					letterSpacing: "-=2" 
				}, time/2.5)
			})
		}

DieSimulator.prototype.animationEnlarge = function(){
			el = this.element
			time = this.time
			el.animate({
				letterSpacing:"2px"
			}, time, function(){
				return el[0].click()
			})
		}

		// time: function(){
		// 	return time
		// },

DieSimulator.prototype.next = function(){
		
			this.element = this.select()

			this.incTime()
		}

DieSimulator.prototype.roll = function(){
	this.animation()
	that = this
		setTimeout( function(){
			that.next()
			if (that.time >= 1000){
				that.animationEnlarge()
				return

			} else {
				that.roll()
			}

		}, that.time)
}
	


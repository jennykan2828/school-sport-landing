var startPosition = 3999 //strating position of .project-card

window.onload = function () {
    shuffleCards()
    attachClickEventCards() //attacth card rotate event each div.project-card
    document.querySelector('.pcon').addEventListener('click', (event)=>{
        let targetCard = document.querySelector('.view')
        if(isRightSideClick(event)){
            putCardEnd(targetCard)
            showNextCard(targetCard)
        }else{      //left side clicked
            putCardStart(targetCard)
            showPrevCard(targetCard)
        }
    }, false)
}


function attachClickEventCards() {
    const cards = document.querySelectorAll('.project-card')
    cards.forEach(card =>{
        card.addEventListener('click',(event)=>{
            event.stopPropagation()     //stop trigger parent click event
            let transformValue = card.style.transform
            transformValue = parseInt(transformValue.split('(')[1].replace(')', ''))
            card.style.transform = `rotateY(${transformValue + 180}deg)`
        }, false)
    })
}

function shuffleCards() {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        putCardStart(card)
    });
    const firstCard = document.querySelector('.project-card')
    viewCard(firstCard)

}
function putCardStart(card) {
    //Place card leftside of viewport 
    card.style.transform = 'rotateY(0deg)' //make sure card was in its initial position
    card.style.left = -startPosition + 'px'
}

function putCardEnd(card) {
    //Place card rightside of viewport 
    card.style.left = startPosition + 'px'
}

function showNextCard(card) {
    //it will show next child card
    let nextSibling = card.nextElementSibling
    let cards = document.querySelectorAll('.project-card')
    if(nextSibling == null){
        viewCard(card)
        shakeCard(card)
        cards.forEach(c=>{
            if(c !== card)  //avoid current card
                putCardStart(c)
        })
        return 
    }
    card.classList.remove('view')       ///remove .view from current 
    viewCard(nextSibling)

}

function showPrevCard(card) {
    //it will show next child card
    let cards = document.querySelectorAll('.project-card')
    let prevSibling = card.previousElementSibling
    if(prevSibling == null){
        // alert("There was no next sibling")
        viewCard(card)
        shakeCard(card)
        return 
    }
    card.classList.remove('view')       ///remove .view from current 
    viewCard(prevSibling)

}


function viewCard(card, direction='right') {
    const cardCon = document.querySelector('.pcon')
    const leftSpace = cardCon.offsetWidth / 4   //x
    card.style.left = leftSpace + 'px'  //formula to place card1 in place was "(wd-cd)+x"
    card.classList.add('view')
    card.dataset.direction = direction
}

function isRightSideClick(event) {
    //This one identify which side clicked of div.pcon
    //true - right side
    //false - left side
    const pcon = document.querySelector('.pcon')        //container
    let pointX = event.x
    if(pcon.offsetWidth / 2 <= pointX)  //right side clicked 
        return true
    return false    //left side clicked
}

function shakeCard(card){
    //apply a skaking effect
    card.classList.add('shakeit')
    setTimeout(()=>{
        card.classList.remove('shakeit')
    }, 500)   
}
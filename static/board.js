
let score = 0;

console.log("board.js called");

const alreadySelectedWords = new Set();

$('.check-word').on("submit", async function(evt) {
  evt.preventDefault();
  let word = $('input').val();
  console.log(word);
  if(alreadySelectedWords.has(word)){
    $('#wordResult').text(`You have already chosen ${word}`);
    return;
  }
  const res = await axios.get('/check-word', {params: {word: word}});
  console.log("res.data.result", res.data.result);
  let response = res.data.result;
  if(response === 'not-on-board'){
    $('#wordResult').text(`${word} is not on the board`);
  }
  else if(response === 'not-word'){
    $('#wordResult').text(`${word} is not a valid word`);
  }
  else{
    $('#wordResult').text(`Well done, that's a good word`);
    alreadySelectedWords.add(word);
    score = score + word.length;
    $('#score').text(score);
  }
  $('input').val('');
});



$('document').ready(function(){
  repeatEverySecond()
})

let intervalID;

function repeatEverySecond(){
    let timeLeft = 60;
    $('#timer').text(timeLeft);
    intervalID = setInterval(function(){
      timeLeft = timeLeft - 1;
      $('#timer').text(timeLeft);
      if(timeLeft === 0){
        clearInterval(intervalID);
        $('form').remove();
        $('#timerTitle').remove();
        $('#wordResult').remove();
        $('#timer').text("Time's up!");
        sendScoreToBackEnd(score);
        }
    }, 1000);
  }


  async function sendScoreToBackEnd(score){
    console.log("sendScoreToBackEnd has been called");
    console.log("score", score);
    const res = await axios.post('/save-score', {score: score});
    console.log("res", res)
  }













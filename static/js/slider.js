let offset = 0; //смещение от левого края
const sliderline= document.querySelector('.slider-line')

document.querySelector('.slider-next').addEventListener('click', function(){
  offset = offset + 915;
  if (offset > 2745){
    offset = 0;
  }
  sliderline.style.left=-offset+'px'
});

document.querySelector('.slider-prev').addEventListener('click', function(){
  offset = offset - 915;
  if (offset < 0){
    offset = 2745;
  }
  sliderline.style.left=-offset+'px'
});

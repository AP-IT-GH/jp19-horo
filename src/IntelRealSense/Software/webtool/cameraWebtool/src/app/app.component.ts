import { Component, HostListener } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'cameraWebtool';

  cursorX : number;
  cursorY : number;
  cursorXCalculated : string;
  cursorYCalculated : string;

  widthDetectionArea : string;
  heightDetectionArea : string;
  widthDetectionAreaNumber : number = 0.00;
  heightDetectionAreaNumber : number = 0.00;

  protected primaryColor: string;
  protected secondaryColor: string;

  constructor(){
    this.primaryColor = "#ffffff";
    this.secondaryColor = "#9f9f9f";
  }

  propState(propState : boolean){
    console.log("editor function is clicked");
    console.log(propState)
    if(propState == true){
      this.editorOn()
    }
    else if(propState == false){
      this.detectedOn()
    }
  }

  editorOn(){
    console.log("chenged to editor view")
    document.getElementById('editorButton').style.backgroundColor = "#F5F5F5"
    document.getElementById('detectedButton').style.backgroundColor = "#D3CFCF"
    document.getElementById('editor').style.visibility = "visible"
    document.getElementById('detected').style.visibility = "hidden"
  }

  detectedOn(){
    console.log("chenged to editor view")
    document.getElementById('editorButton').style.backgroundColor = "#D3CFCF"
    document.getElementById('detectedButton').style.backgroundColor = "#F5F5F5"
    document.getElementById('editor').style.visibility = "hidden"
    document.getElementById('detected').style.visibility = "visible"
  }

  @HostListener('mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    //console.log(event.pageX + " " + event.pageY);
    const walk = 100; //100px max offset distance
    
    var width = document.getElementById('field').offsetWidth;
    var height = document.getElementById('field').offsetHeight;

    if(width >= event.pageX){
      this.cursorX = event.pageX;
      this.cursorXCalculated = ((this.cursorX / width) * this.widthDetectionAreaNumber).toFixed(3);
    }
    
    if(event.pageY <= 480){ //Hardcoded must be changed to auto later on!!
      this.cursorY = event.pageY;
      this.cursorYCalculated = ((this.cursorY / 480) * this.heightDetectionAreaNumber).toFixed(3);
    }
    
    this.widthDetectionArea = this.widthDetectionAreaNumber + "m";
    this.heightDetectionArea = this.heightDetectionAreaNumber + "m";
    //console.log(event.pageX + " " + event.pageY);
    //console.log(height);
  }
}

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
    //console.log(propState)
    if(propState == true){
      console.log("editor function is clicked");
      this.editorOn()
    }
    else if(propState == false){
      console.log("detected function is clicked");
      this.detectedOn()
    }
  }

  editorOn(){
    console.log("chenged to editor view");
    document.getElementById('editorButton').style.backgroundColor = "#F5F5F5";
    document.getElementById('detectedButton').style.backgroundColor = "#D3CFCF";
    document.getElementById("editor").style.display = "inline";
    document.getElementById("detected").style.display = "none";
    console.log(document.getElementById("detected").style.display);
  }

  detectedOn(){
    console.log("chenged to detected view");
    document.getElementById('editorButton').style.backgroundColor = "#D3CFCF";
    document.getElementById('detectedButton').style.backgroundColor = "#F5F5F5";
    document.getElementById("editor").style.display = "none";
    document.getElementById("detected").style.display = "inline";
    console.log(document.getElementById("detected").style.display);
  }

  addButton(){
    this.addElement();
  }

  @HostListener('mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    //console.log(event.pageX + " " + event.pageY);
    const walk = 100; //100px max offset distance
    
    var width = document.getElementById('field').offsetWidth;
    var height = document.getElementById('field').offsetHeight;

    if(width >= event.pageX && event.pageY <= 480){
      this.cursorX = event.pageX;
      this.cursorXCalculated = ((this.cursorX / width) * this.widthDetectionAreaNumber).toFixed(3);
      this.cursorY = event.pageY;
      this.cursorYCalculated = ((this.cursorY / 480) * this.heightDetectionAreaNumber).toFixed(3);
    }
    /*
    if(width >= event.pageX){
      this.cursorX = event.pageX;
      this.cursorXCalculated = ((this.cursorX / width) * this.widthDetectionAreaNumber).toFixed(3);
    }
    
    if(event.pageY <= 480){ //Hardcoded must be changed to auto later on!!
      this.cursorY = event.pageY;
      this.cursorYCalculated = ((this.cursorY / 480) * this.heightDetectionAreaNumber).toFixed(3);
    }*/
    
    this.widthDetectionArea = this.widthDetectionAreaNumber + "m";
    this.heightDetectionArea = this.heightDetectionAreaNumber + "m";
    //console.log(event.pageX + " " + event.pageY);
    //console.log(height);
  }

  //document.body.onload = addElement;

  maskNumber : number = 1;

  addElement () { 
    var node = document.createElement("div");
    var textnode = document.createTextNode("Mask " + this.maskNumber);
    node.appendChild(textnode);

    node.id = this.maskNumber.toString();

    //node styling
    var nodeStyle = node.style; 
    nodeStyle.width = "80%";
    nodeStyle.backgroundColor = "white";
    nodeStyle.marginLeft = "auto";
    nodeStyle.marginRight = "auto";
    nodeStyle.height = "60px";
    nodeStyle.borderRadius = "15px";
    nodeStyle.marginTop = "25px";
    nodeStyle.borderStyle = "solid";
    nodeStyle.borderWidth = "4px";
    nodeStyle.borderColor = "#2680EB";

    document.getElementById("maskDivsContainer").appendChild(node);

    this.addInputFieldInElement(this.maskNumber);

    this.maskNumber += 1;
  }

  addInputFieldInElement(maskId:number){
    var node = document.createElement("input");
    var textnode = document.createTextNode("0");
    node.appendChild(textnode);
    document.getElementById(maskId.toString()).appendChild(node);
  }
}

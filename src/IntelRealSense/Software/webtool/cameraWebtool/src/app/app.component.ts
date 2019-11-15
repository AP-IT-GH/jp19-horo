import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'cameraWebtool';

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
}

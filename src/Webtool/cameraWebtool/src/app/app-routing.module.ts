import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


const routes: Routes = [];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 


  propState(editorState:boolean) {
    console.log("de boolean is " + String(editorState))
    if(editorState == true){
      document.getElementById("editorButton").style.backgroundColor = "#F5F5F5;";
      document.getElementById("detectedButton").style.backgroundColor = "#D3CFCF";
      document.getElementById("").style.visibility = "hidden";
      document.getElementById("").style.visibility = "visible"
    }
    if(editorState == false){
      document.getElementById("editorButton").style.backgroundColor = "#D3CFCF;";
      document.getElementById("detectedButton").style.backgroundColor = "#F5F5F5";
      document.getElementById("").style.backgroundColor = "";
      document.getElementById("").style.visibility = "hidden";
      document.getElementById("").style.visibility = "visible"
    }
    
  }
}

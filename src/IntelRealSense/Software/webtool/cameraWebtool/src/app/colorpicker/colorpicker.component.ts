import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-colorpicker',
  templateUrl: './colorpicker.component.html',
  styleUrls: ['./colorpicker.component.css']
})
export class ColorpickerComponent implements OnInit {

  protected primaryColor: string;
  protected secondaryColor: string;

  constructor() {
    this.primaryColor = '#FF100D';
    this.secondaryColor = '#EFFAF7';
   }

  ngOnInit() {
  }

}

import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ColorpickerComponent } from './colorpicker/colorpicker.component';

import {WebcamModule} from 'ngx-webcam';
import { ColorPickerModule } from 'ngx-color-picker';
import { from } from 'rxjs';

@NgModule({
  declarations: [
    AppComponent,
    ColorpickerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    WebcamModule,
    ColorPickerModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

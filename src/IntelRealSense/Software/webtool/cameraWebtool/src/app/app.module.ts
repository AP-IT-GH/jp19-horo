import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ColorpickerComponent } from './colorpicker/colorpicker.component';

import {WebcamModule} from 'ngx-webcam';
import { ColorPickerModule } from 'ngx-color-picker';
import { NgxMqttClientModule } from 'ngx-mqtt-client';

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
    NgxMqttClientModule.withOptions({
      manageConnectionManually: true, // this flag will prevent the service to connection automatically
      host: 'broker.hivemq.com',
      protocol: 'ws',
      port: 8000,
      path: '/mqtt'
  })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

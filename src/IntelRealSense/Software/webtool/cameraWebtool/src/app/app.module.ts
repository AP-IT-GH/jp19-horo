import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ColorpickerComponent } from './colorpicker/colorpicker.component';

import {WebcamModule} from 'ngx-webcam';
import { ColorPickerModule } from 'ngx-color-picker';
import { NgxMqttClientModule } from 'ngx-mqtt-client';
import { MqttModule, IMqttServiceOptions } from 'ngx-mqtt';
import { from } from 'rxjs';
import { MaskComponent } from './mask/mask.component';


// export const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
//   hostname: 'broker.mqttdashboard.com',
//   port: 8000,
//   path: '/mqtt'
// };


export const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: '192.168.0.69',
  port: 1883,
  path: '/'
};

@NgModule({
  declarations: [
    AppComponent,
    ColorpickerComponent,
    MaskComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    WebcamModule,
    ColorPickerModule,
    FormsModule,
    MqttModule.forRoot(MQTT_SERVICE_OPTIONS),
  //   NgxMqttClientModule.withOptions({
  //     // manageConnectionManually: true, //this flag will prevent the service to connection automatically
  //     host: 'broker.mqttdashboard.com',
  //     protocol: 'ws',
  //     port: 8000,
  //     path: '/mqtt'
  // })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

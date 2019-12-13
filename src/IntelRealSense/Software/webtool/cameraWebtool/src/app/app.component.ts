import { Component, OnDestroy, OnInit, ElementRef, ViewChild } from '@angular/core';
import { IMqttMessage, MqttModule, IMqttServiceOptions, MqttService } from 'ngx-mqtt';
import { Subscription } from 'rxjs';
import { ConnectionStatus } from 'ngx-mqtt-client';


export const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
  hostname: 'localhost',
  port: 9001,
  path: '/mqtt'
};

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnDestroy {
  private subscription: Subscription;
  public topicname: any;
  public msg: any;
  isConnected: boolean = false;

  protected xstring: string;
  protected ystring: string;
  protected zstring: string;


  public message: string;

  messages: Array<Foo> = [];
  status: Array<string> = [];


  @ViewChild('msglog', { static: true }) msglog: ElementRef;

  title = 'cameraWebtool';

  protected primaryColor: string;
  protected secondaryColor: string;

  constructor(private _mqttService: MqttService){
    this.primaryColor = "#ffffff";
    this.secondaryColor = "#9f9f9f";
    this.message = "Hallo we zijn aan het testen";
    this.topicname = 'webtoolrobotarm';
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

  subscribeNewTopic(): void {
    console.log('inside subscribe new topic')
    this.subscription = this._mqttService.observe(this.topicname).subscribe((message: IMqttMessage) => {
      this.msg = message;
      console.log('msg: ', message)
      this.logMsg('Message: ' + message.payload.toString() + '<br> for topic: ' + message.topic);
    });
    this.logMsg('subscribed to topic: ' + this.topicname)


  }

  sendmsg(): void {
    this.SetStringMessage();
    // use unsafe publish for non-ssl websockets
    this._mqttService.unsafePublish(this.topicname, this.msg, { qos: 1, retain: true })
    this.ResetStrings();
    console.log(this._mqttService.observe('test').pipe());
  }

  private SetStringMessage(){
    this.msg = this.xstring + ';' + this.ystring + ';' + this.zstring + ';';
  }

  private ResetStrings(){
    this.xstring = '';
    this.ystring = '';
    this.zstring = '';
    this.msg = '';
  }

  logMsg(message): void {
    this.msglog.nativeElement.innerHTML += '<br><hr>' + message;
  }

  clear(): void {
    this.msglog.nativeElement.innerHTML = '';
  }

  IncomingMessageService(){

  }

  GetMessages() {
    console.log('1');
    console.log(this._mqttService.onPacketreceive);
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

  public unsafePublish(topic: string, message: string): void {
    this._mqttService.unsafePublish(topic, message, {qos: 1, retain: true});
  }

  public ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}

export interface Foo {
  bar: string;
}

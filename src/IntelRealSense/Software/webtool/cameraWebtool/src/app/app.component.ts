import { Component, OnDestroy, OnInit, ElementRef, ViewChild, HostListener } from '@angular/core';
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

  constructor(private _mqttService: MqttService){
    this.primaryColor = "#ffffff";
    this.secondaryColor = "#9f9f9f";
    this.message = "Hallo we zijn aan het testen";
    this.topicname = 'webtoolrobotarm';
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

  addElement() {
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

    this.addWidthFieldInElement(this.maskNumber);
    this.addHeightFieldInElement(this.maskNumber);
    this.addXPositionFieldInElement(this.maskNumber);
    this.addYPositionFieldInElement(this.maskNumber);
    this.addRotationFieldInElement(this.maskNumber);

    this.maskNumber += 1;
  }

  addWidthFieldInElement(maskId:number){
    var node = document.createElement("input");

    node.id = "widthInput" + maskId;
    node.placeholder = "width";

    var nodeStyle = node.style;
    nodeStyle.borderRadius = "15px";
    nodeStyle.borderStyle = "solid";
    nodeStyle.borderWidth = "2px";
    nodeStyle.borderColor = "black"
    nodeStyle.height = "25px";
    nodeStyle.width = "52px";


    var textnode = document.createTextNode("0");
    node.appendChild(textnode);
    document.getElementById(maskId.toString()).appendChild(node);
  }

  addHeightFieldInElement(maskId:number){
    var node = document.createElement("input");

    node.id = "heightInput" + maskId;
    node.placeholder = "height";

    var nodeStyle = node.style;
    nodeStyle.borderRadius = "15px";
    nodeStyle.borderStyle = "solid";
    nodeStyle.borderWidth = "2px";
    nodeStyle.borderColor = "black"
    nodeStyle.height = "25px";
    nodeStyle.width = "52px";


    var textnode = document.createTextNode("0");
    node.appendChild(textnode);
    document.getElementById(maskId.toString()).appendChild(node);
  }

  addXPositionFieldInElement(maskId:number){
    var node = document.createElement("input");

    node.id = "xPositionInput" + maskId;
    node.placeholder = "x position";

    var nodeStyle = node.style;
    nodeStyle.borderRadius = "15px";
    nodeStyle.borderStyle = "solid";
    nodeStyle.borderWidth = "2px";
    nodeStyle.borderColor = "black"
    nodeStyle.height = "25px";
    nodeStyle.width = "52px";


    var textnode = document.createTextNode("0");
    node.appendChild(textnode);
    document.getElementById(maskId.toString()).appendChild(node);
  }

  addYPositionFieldInElement(maskId:number){
    var node = document.createElement("input");

    node.id = "yPositionInput" + maskId;
    node.placeholder = "y position";

    var nodeStyle = node.style;
    nodeStyle.borderRadius = "15px";
    nodeStyle.borderStyle = "solid";
    nodeStyle.borderWidth = "2px";
    nodeStyle.borderColor = "black"
    nodeStyle.height = "25px";
    nodeStyle.width = "52px";


    var textnode = document.createTextNode("0");
    node.appendChild(textnode);
    document.getElementById(maskId.toString()).appendChild(node);
  }

  addRotationFieldInElement(maskId:number){
    var node = document.createElement("input");

    node.id = "rotationInput" + maskId;
    node.placeholder = "rotation";

    var nodeStyle = node.style;
    nodeStyle.borderRadius = "15px";
    nodeStyle.borderStyle = "solid";
    nodeStyle.borderWidth = "2px";
    nodeStyle.borderColor = "black"
    nodeStyle.height = "25px";
    nodeStyle.width = "52px";


    var textnode = document.createTextNode("0");
    node.appendChild(textnode);
    document.getElementById(maskId.toString()).appendChild(node);
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

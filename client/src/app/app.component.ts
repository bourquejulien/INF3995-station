import { Component } from '@angular/core';
import {CommandService} from "@app/services/command.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'web-ui';

  constructor(private commandService: CommandService) {
  }

  init() {
    this.commandService.initFlight('0');
  }

  takeOff() {
    this.commandService.takeoff('0');
  }
}

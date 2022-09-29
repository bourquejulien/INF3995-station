import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommandService } from '@app/services/command/command.service';

@Component({
  selector: 'app-mission-page',
  templateUrl: './mission-page.component.html',
  styleUrls: ['./mission-page.component.css']
})
export class MissionPageComponent implements OnInit {

  constructor(private router:Router, public commandService:CommandService) {
    this.selectedUris = []
  }

  selectedUris: string[]

  ngOnInit(): void {
    this.commandService.discover()
  }

  identify() : void {
    if (this.selectedUris.length == 0) {
      return
    }
    this.commandService.identify({uris: this.selectedUris})
  }

  start_mission() : void {
    this.commandService.start_mission({})
  }

  end_mission() : void {
    this.commandService.end_mission({})
  }

}

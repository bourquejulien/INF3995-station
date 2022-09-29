import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommandService } from '@app/services/command/command.service';

@Component({
  selector: 'app-mission-page',
  templateUrl: './mission-page.component.html',
  styleUrls: ['./mission-page.component.css']
})
export class MissionPageComponent implements OnInit {

  constructor(private router:Router, private commandService:CommandService) {
  }

  ngOnInit(): void {
  }

  initialize() : void {
    this.commandService.initialize({drones: []})
  }

  start_mission() : void {
    this.commandService.start_mission({drones: []})
  }

  end_mission() : void {
    this.commandService.end_mission({drones: []})
  }

}
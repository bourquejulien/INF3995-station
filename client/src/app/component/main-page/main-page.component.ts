import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommandService } from '@app/services/command/command.service';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css']
})
export class MainPageComponent implements OnInit {
  readonly title: string = 'Système aérien d’exploration';

  constructor(private router:Router, private commandService:CommandService) {
  }

  startSimulation() : void {
    this.commandService.set_up({isSimulation: true})
    this.router.navigateByUrl("/mission"); // go to the mission page
  }

  startDrone() : void {
    this.commandService.set_up({isSimulation: false})
    this.router.navigateByUrl("/mission"); // go to the mission page
  }

  ngOnInit(): void {
  }

}

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
    this.commandService.init({command: "init", isSimulation: true})
    this.router.navigateByUrl("/mission");
  }

  startDrone() : void {
    this.commandService.init({command: "init", isSimulation: false})
    this.router.navigateByUrl("/mission");
  }

  ngOnInit(): void {
  }

}

import { Component, OnInit } from '@angular/core';
import { FirmwareService } from '@app/services/firmware/firmware.service';
import { PartialObserver } from 'rxjs';

type Mode = "file" | "editor";

@Component({
  selector: 'app-firmware-panel',
  templateUrl: './firmware-panel.component.html',
  styleUrls: ['./firmware-panel.component.css']
})
export class FirmwarePanelComponent implements OnInit {
    collapsed: boolean;
    isFlashError: boolean;
    isFlashing: boolean;
    currentMode: Mode;
    modes: Array<[Mode, string]>;
    file: File | null;

    constructor(protected firmwareService: FirmwareService) {
        this.collapsed = true;
        this.isFlashError = false;
        this.isFlashing = false;
        this.currentMode = "file";
        this.modes = [["file", "Téléversement"],["editor", "Depuis un fichier"]]
        this.file = null;
    }

    ngOnInit(): void {
        this.isFlashError = false;
        this.isFlashing = false;
        this.currentMode = "file";
        this.file = null;
    }

    getName(mode: Mode): string {
        return this.modes.filter(e => e[0] == mode).map(e => e[1])[0];
    }

    selectMode(mode: Mode): void {
       this.currentMode = mode;
       this.collapsed = true;
       this.file = null;
    }

    setFile(event: Event) : void {
        const input: any = event.target as HTMLInputElement;
        this.file = input.files[0]
    }

    flash(): void {
        this.isFlashError = false;
        if (this.currentMode == "editor")
        {
            this.firmwareService.buildFlash().subscribe(this.flashHandler());
        }

        if (this.file == null){
            return;
        }

        this.firmwareService.flashFile(this.file).subscribe(this.flashHandler());
    }

    private flashHandler() {
        this.isFlashing = true;
        return {
            complete: () => this.isFlashing = false,
            error: (err: string) => {
                this.isFlashError = true;
                this.isFlashing = false;
            },
        }
    }
}

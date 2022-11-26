(function () {
    const grid = document.getElementById('scheme-grid');
        let cellsElems = [];
        let sensorsInfo = null;
        for (let i = 0; i < 12; i++) {
            let row = document.createElement('div');
            row.className = 'row';
            row.style.height = '3.5rem';
            for (let j = 0; j < 12; j++) {
                let cell = document.createElement('div');
                cell.className = 'col text-center';
                cellsElems.push(cell);
                row.appendChild(cell);
            }
            grid.appendChild(row);
        }

        for (let i = 0; i < cellsElems.length; i++) {
            let item = cellsElems[i];

            item.onmouseover = cellOnmouseover;
            item.onmouseout = cellOnmouseout;
            item.addEventListener('dragstart', dragStart);
            item.addEventListener('dragover', dragOver);
            item.addEventListener('drop', drop);
            item.id = i;
        }

        function upd_cells() {
            cellsElems.forEach((item) => {
                let unPos = 0;
                for (const dataKey in sensorsInfo) {
                    let vol = sensorsInfo[dataKey][0];
                    let pos = sensorsInfo[dataKey][1];
                    let name = sensorsInfo[dataKey][2];
                    if (pos === -1) {
                        pos = unPos;
                        unPos++;
                    }
                    cellsElems[pos].setAttribute('data-sensor-id', dataKey);
                    if (name.length > 24) {
                        cellsElems[pos].innerHTML = '<small>' + name.substring(0, 12)  + ' ... ' + name.substring(name.length - 12) + '</small>' + '<br>' + vol;
                    } else {
                        cellsElems[pos].innerHTML = '<small>' + name + '</small>' + '<br>' + vol;
                    }
                }
                if (item.hasAttribute('data-sensor-id')) {
                    item.draggable = true;
                    item.style = 'background: rgba(190, 190, 255, 0.7)';
                } else {
                    item.removeAttribute('data-sensor-id');
                    item.removeAttribute('draggable');
                    item.removeAttribute('style');
                    item.innerText = '';
                }
            });
        }

        function api_grid_upd() {
            let request = window.location.origin + "/new/api/scheme/grid";
            const urlParams = new URLSearchParams(window.location.search);
            jQuery.get(request, {'object_id': urlParams.get('object_id')},
                function (data) {
                    sensorsInfo = data;
                    upd_cells();
                }
            );
        }


        function cellOnmouseover() {
            this.style = 'background: rgba(114, 103, 239, 0.6)';
        }

        function cellOnmouseout() {
            this.removeAttribute('style');
            if (this.hasAttribute('data-sensor-id')) {
                this.style = 'background: rgba(190, 190, 255, 0.7)';
            }
        }

        function dragStart(evt) {
            evt.dataTransfer.setData('id', this.id);
            evt.dataTransfer.effectAllowed = 'move';
        }

        function dragOver(evt) {
            evt.dataTransfer.dropEffect = 'move';
            evt.preventDefault();
        }

        function drop(evt) {
            const s = evt.dataTransfer.getData('id');
            if (s && s !== this.id) {
                let sensor_id = cellsElems[s].getAttribute('data-sensor-id');
                cellsElems[s].removeAttribute('data-sensor-id');

                this.setAttribute('data-sensor-id', sensor_id);
                sensorsInfo[sensor_id][1] = this.id;
                evt.preventDefault();
                upd_cells();

                let context = {};
                let request = window.location.origin + "/new/api/scheme/save";
                for (const key in sensorsInfo) {
                    context[key] = sensorsInfo[key][1];
                }
                jQuery.get(request, context);
            }
        }

        jQuery(document).ready(api_grid_upd);
        setInterval(api_grid_upd, 60000);
})()

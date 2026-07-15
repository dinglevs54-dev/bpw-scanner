<script>
    let currentLogs = null;
    let pieChart = null;
    
    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        
        document.getElementById(`page-${pageId}`).classList.add('active');
        event.currentTarget.classList.add('active');
    }
    
    async function generatePin() {
        const res = await fetch('/api/generate-pin');
        const data = await res.json();
        document.getElementById('pin-display').innerText = data.pin;
    }
    
    async function fetchLogs() {
        const pin = document.getElementById('fetch-pin').value;
        if(pin.length !== 6) { alert("Please enter a 6-digit code"); return; }
        
        const output = document.getElementById('log-output');
        output.innerHTML = '<div style="color: #7877c6; text-align: center; padding: 40px;">⏳ Fetching logs...</div>';
        
        try {
            const res = await fetch(`/api/get-logs/${pin}`);
            const data = await res.json();
            
            if (data.status === 'success') {
                currentLogs = data.logs;
                updateOverview(data.logs);
                populateAllSections(data.logs);
                
                output.innerHTML = '<div style="color: #06b6d4; text-align: center; padding: 20px;">✅ Logs loaded successfully!<br>Navigate through the sections to view detailed findings.</div>';
            } else {
                output.innerText = " Error: " + data.message;
            }
        } catch (e) {
            output.innerText = "❌ Error fetching logs: " + e;
        }
    }
    
    function updateOverview(logs) {
        let detections = 0;
        let warnings = 0;
        let information = 0;
        
        if (logs.findings) {
            logs.findings.forEach(finding => {
                const severity = finding.severity || 'INFO';
                if (severity === 'CRITICAL' || severity === 'HIGH') {
                    detections++;
                } else if (severity === 'MEDIUM') {
                    warnings++;
                } else {
                    information++;
                }
            });
        }
        
        document.getElementById('stat-detections').innerText = detections;
        document.getElementById('stat-warnings').innerText = warnings;
        document.getElementById('stat-information').innerText = information;
        document.getElementById('stat-total').innerText = logs.total_findings || 0;
        document.getElementById('top-warnings').innerText = warnings;
        document.getElementById('top-detections').innerText = detections;
        
        drawPieChart(detections, warnings, information);
    }
    
    function populateAllSections(logs) {
        if (!logs.findings || logs.findings.length === 0) {
            return;
        }
        
        // Categorize findings
        const categories = {
            discord: [],
            processes: [],
            files: [],
            deletedFiles: [],
            prefetch: [],
            dma: [],
            logs: [],
            general: []
        };
        
        logs.findings.forEach(finding => {
            const type = finding.type || '';
            
            if (type.includes('Discord')) {
                categories.discord.push(finding);
            } else if (type.includes('Process')) {
                categories.processes.push(finding);
            } else if (type.includes('Deleted')) {
                categories.deletedFiles.push(finding);
            } else if (type.includes('Prefetch')) {
                categories.prefetch.push(finding);
            } else if (type.includes('DMA') || type.includes('Device')) {
                categories.dma.push(finding);
            } else if (type.includes('Log')) {
                categories.logs.push(finding);
            } else if (type.includes('File') && !type.includes('Deleted')) {
                categories.files.push(finding);
            } else {
                categories.general.push(finding);
            }
        });
        
        // Populate General Information
        const generalContent = document.getElementById('general-content');
        if (categories.general.length > 0 || categories.logs.length > 0) {
            let html = '';
            
            // Add scan info
            html += `
                <div style="background: rgba(120, 119, 198, 0.1); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <div style="color: #888; font-size: 12px; margin-bottom: 5px;">📅 Scan Time</div>
                            <div style="color: #fff; font-weight: 600;">${logs.timestamp || 'Unknown'}</div>
                        </div>
                        <div>
                            <div style="color: #888; font-size: 12px; margin-bottom: 5px;">💻 Hostname</div>
                            <div style="color: #fff; font-weight: 600;">${logs.hostname || 'Unknown'}</div>
                        </div>
                        <div>
                            <div style="color: #888; font-size: 12px; margin-bottom: 5px;">👤 Username</div>
                            <div style="color: #fff; font-weight: 600;">${logs.username || 'Unknown'}</div>
                        </div>
                        <div>
                            <div style="color: #888; font-size: 12px; margin-bottom: 5px;">📊 Total Findings</div>
                            <div style="color: #fff; font-weight: 600;">${logs.total_findings || 0}</div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add log tampering warnings
            if (categories.logs.length > 0) {
                html += '<div style="margin-bottom: 20px;"><div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;">⚠️ Log Tampering Detected</div>';
                categories.logs.forEach(item => {
                    const badgeClass = getBadgeClass(item.severity);
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="color: #fff; font-weight: 600;">${item.file}</div>
                                <span class="badge ${badgeClass}">${item.severity}</span>
                            </div>
                            <div style="color: #888; font-size: 13px; margin-top: 8px;">${item.reason}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            // Add other general findings
            if (categories.general.length > 0) {
                html += '<div><div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;">📋 General Findings</div>';
                categories.general.forEach(item => {
                    const badgeClass = getBadgeClass(item.severity);
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="color: #fff; font-weight: 600;">${item.type}</div>
                                <span class="badge ${badgeClass}">${item.severity}</span>
                            </div>
                            <div style="color: #888; font-size: 13px; margin-top: 8px;">${item.file} - ${item.reason}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            generalContent.innerHTML = html;
        }
        
        // Populate File Activity
        const fileContent = document.querySelector('#page-files .glass-panel > div:last-child');
        if (fileContent) {
            let html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">';
            
            // Cheats/Suspicious Files
            html += '<div><div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;"> Suspicious Files Found</div>';
            if (categories.files.length > 0) {
                categories.files.forEach(item => {
                    const badgeClass = getBadgeClass(item.severity);
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <div style="color: #fff; font-weight: 600; font-family: monospace;">${item.file}</div>
                                <span class="badge ${badgeClass}">${item.severity}</span>
                            </div>
                            <div style="color: #888; font-size: 12px; margin-bottom: 8px;">${item.path || 'Path unknown'}</div>
                            <div style="color: #f59e0b; font-size: 13px;">${item.reason}</div>
                            ${item.hash ? `<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); font-family: monospace; font-size: 11px; color: #666;">${item.hash.substring(0, 32)}...</div>` : ''}
                        </div>
                    `;
                });
            } else {
                html += '<div style="color: #666; text-align: center; padding: 30px;">No suspicious files found</div>';
            }
            html += '</div>';
            
            // Deleted Files
            html += '<div><div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;">🗑️ Deleted Executables</div>';
            if (categories.deletedFiles.length > 0) {
                categories.deletedFiles.forEach(item => {
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="color: #fff; font-weight: 600; font-family: monospace; margin-bottom: 8px;">${item.file}</div>
                            <div style="color: #06b6d4; font-size: 13px; margin-bottom: 5px;">⏰ ${item.timestamp || 'Unknown time'}</div>
                            <div style="color: #888; font-size: 13px;">${item.reason}</div>
                            ${item.note ? `<div style="color: #f59e0b; font-size: 12px; margin-top: 5px;">⚠️ ${item.note}</div>` : ''}
                        </div>
                    `;
                });
            } else {
                html += '<div style="color: #666; text-align: center; padding: 30px;">No deleted executables found</div>';
            }
            html += '</div></div>';
            
            fileContent.innerHTML = html;
        }
        
        // Populate Suspicious Entries
        const suspiciousContent = document.querySelector('#page-suspicious .glass-panel > div:last-child');
        if (suspiciousContent) {
            let html = '';
            
            // Prefetch artifacts
            if (categories.prefetch.length > 0) {
                html += '<div style="margin-bottom: 30px;"><div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;">📀 Prefetch Artifacts</div>';
                categories.prefetch.forEach(item => {
                    const badgeClass = getBadgeClass(item.severity);
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="color: #fff; font-weight: 600; font-family: monospace;">${item.file}</div>
                                <span class="badge ${badgeClass}">${item.severity}</span>
                            </div>
                            <div style="color: #f59e0b; font-size: 13px; margin-top: 8px;">${item.reason}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            // DMA Devices
            if (categories.dma.length > 0) {
                html += '<div><div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;">🔌 Suspicious Devices</div>';
                categories.dma.forEach(item => {
                    html += `
                        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="color: #ef4444; font-weight: 700; margin-bottom: 8px;">🚨 ${item.file}</div>
                            <div style="color: #fff; font-size: 13px;">${item.reason}</div>
                            <div style="color: #888; font-size: 12px; margin-top: 5px;">Device ID: ${item.device_id || 'Unknown'}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }
            
            if (html === '') {
                html = '<div style="color: #666; text-align: center; padding: 40px;">No suspicious entries found</div>';
            }
            
            suspiciousContent.innerHTML = html;
        }
        
        // Populate Alt Accounts (Discord)
        const accountsContent = document.querySelector('#page-accounts .glass-panel > div:last-child');
        if (accountsContent) {
            if (categories.discord.length > 0) {
                let html = '<div style="color: #fff; font-weight: 700; margin-bottom: 15px; font-size: 18px;"> Discord Accounts Detected</div>';
                categories.discord.forEach(item => {
                    html += `
                        <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <div style="color: #06b6d4; font-weight: 600; margin-bottom: 8px;">${item.file}</div>
                            <div style="color: #fff; font-size: 13px;">${item.reason}</div>
                        </div>
                    `;
                });
                accountsContent.innerHTML = html;
            } else {
                accountsContent.innerHTML = '<div style="color: #666; text-align: center; padding: 40px;">No alternative accounts found</div>';
            }
        }
    }
    
    function getBadgeClass(severity) {
        const map = {
            'CRITICAL': 'badge-critical',
            'HIGH': 'badge-high',
            'MEDIUM': 'badge-medium',
            'INFO': 'badge-info'
        };
        return map[severity] || 'badge-info';
    }
    
    function drawPieChart(detections, warnings, information) {
        const ctx = document.getElementById('pieChart').getContext('2d');
        
        if (pieChart) {
            pieChart.destroy();
        }
        
        // Only create chart if there's data
        const total = detections + warnings + information;
        if (total === 0) {
            document.querySelector('.chart-container').innerHTML = '<div style="color: #666; text-align: center; padding: 40px;">No data to display</div>';
            return;
        }
        
        pieChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Detections', 'Warnings', 'Information'],
                datasets: [{
                    data: [detections, warnings, information],
                    backgroundColor: [
                        'rgba(239, 68, 68, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(6, 182, 212, 0.8)'
                    ],
                    borderColor: [
                        'rgba(239, 68, 68, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(6, 182, 212, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { 
                            color: '#fff', 
                            padding: 20,
                            font: { family: 'Inter', size: 14 }
                        }
                    }
                }
            }
        });
    }
</script>

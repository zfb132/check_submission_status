#!/bin/bash

# 默认安装目录
install_dir="/etc/check_submission_status"

service="[Unit]
Description=Check Submission Status service
After=network.target
Wants=check_submission_status.timer

[Service]
Type=oneshot
User=${USER}
WorkingDirectory=${install_dir}
ExecStart=/usr/bin/python3 main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target"

timer="[Unit]
Description=Check Submission Status timer
Requires=check_submission_status.service

[Timer]
Unit=check_submission_status.service
RandomizedDelaySec = 1h
OnCalendar=*-*-* 01,12:00:00 UTC
Persistent=yes

[Install]
WantedBy=timers.target"

if [[ "install" == $1 ]]; then
    echo "$service" > /etc/systemd/system/check_submission_status.service
    echo "$timer" > /etc/systemd/system/check_submission_status.timer
    if [ ! -d "${install_dir}" ];then
        sudo mkdir -p "${install_dir}"
    fi
    sudo cp -rv $(pwd)/* "${install_dir}"
    sudo systemctl enable check_submission_status.timer
    sudo systemctl start check_submission_status.timer
    echo "Installed to ${install_dir} successfully."
    echo "useful commands:"
    echo "  systemctl status check_submission_status       view service status."
    echo "  journalctl -u check_submission_status.timer    view the logs."
    echo "config file: ${install_dir}/config.py"
                
elif [[ "uninstall" == $1 ]]; then
    sudo systemctl disable check_submission_status.timer
    sudo rm /etc/systemd/system/check_submission_status.service
    sudo rm /etc/systemd/system/check_submission_status.timer
    # 提示用户是否要删除安装目录
    read -p "Do you want to delete the directory (${install_dir})? [y/n]" answer
    if [[ "y" == $answer ]]; then
        sudo rm -rf ${install_dir}
    fi
    sudo systemctl daemon-reload
    echo "uninstalled"
else
    echo "Tips:"
    echo "  $0 install      install the check_submission_status systemd service."
    echo "  $0 uninstall    uninstall the check_submission_status service."
fi
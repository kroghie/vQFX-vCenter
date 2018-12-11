# vQFX-vCenter
Deploys vQFX on vCenter via Ansible

This is tested with Ansible 2.7.2, ESXi 6.7, vCSA 6.7 and vQFX 17.4 Vagrantbox. This is provided as-is, the playbook is created for my own lazy sake, and will not be developed much further, nor regulary.

Requirements:

- Ansible 2.7.2
- vQFX downloaded from https://www.juniper.net/us/en/dm/free-vqfx-trial/ - This is verified with vQFX 17.4 Vagrant
- vCenter
- Python and pyVmomi installed (https://pypi.org/project/pyvmomi/)

Instructions:

1) Install Ansible, python and pyVmomi using your favorite tool
2) Download vQFX Vagrantbox files from above link to /var/tmp. If /var/tmp is not prefereable, edit the vars in deploy-vqfx-vcenter to match the location of .box files
3) Edit the variables in the playbook to match your enviroment.
4) Run the ansible playbook with the mandatory parameters -k and -u: `ansible-playbook deploy-vqfx-vcenter.yml -k -u <esxiusername>` - Type in the password for the esxi user when prompted. 
**If you dont provide -k and -u, Ansible will default to using SSH keys and will fail to run correctly, unless you have SSH keys setup to the given ESXi host**


**Tip:**
use -e "key=value" for providing other values for keys instead of editing the playbook everytime.
E.g: `ansible-playbook deploy-vqfx-vcenter.yml -k -u root -e "re_vm_name=vQFX-02"`
More information on using extra variables here;
https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#passing-variables-on-the-command-line

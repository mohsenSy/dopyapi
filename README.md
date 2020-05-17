# Digital Ocean API Client in Python

This project creates a python package called `dopyapi`, used to manage
resources in Digital Ocean cloud.

## Installation

Right now we only provide the ability to install using this repository,
we will publish this package to Python Package Index soon.

```bash
pip3 install https://github.com/mohsenSy/dopyapi.git
```

## Obtain Access Token
To be able to use the API, you must create an access token from
your Digital Ocean account, it can be created [here](https://cloud.digitalocean.com/account/api/tokens).

Copy the token once created and put it in an environment variable
called `DO_TOKEN` by adding this line to `~/.bashrc`

```
export DO_TOKEN=<Your access token here>
```

The library by default uses this environment variable to get the access
token if not provided in the code.

## List and create droplets

The following code is a very basic one that creates a new Droplet
and lists all existing droplets, printing their information as JSON.

```python
import dopyapi as do
do.authenticate()

droplet_data = {
  "name": "d1",
  "region": "ams3",
  "image": do.images.ubuntu,
  "size": do.sizes.tiny,
  "ssh_keys": do.SSHKey.list()
}
droplet = do.Droplet()
droplet.create(**droplet_data)

droplets = do.Droplet.list()
for droplet in droplets:
  print(droplet.json())
```

The previous code creates a new droplet with these attributes:
* name is "d1"
* region is "ams3"
* image is "ubuntu-18-04-x64", here we used a constant value defined
  in the library to help us create droplets  based on popular images
  without having to memorize image slugs or IDs.
* size is "s-1vcpu-1gb", again we used a constant to avoid remembering
  the size slug.
* ssh_keys is set to all keys found in my account, this is optional
  but I prefer to use it every time a new droplet is created.

After that we list droplets and print their JSON information.

For more information about how to use the library, checks docs
found [here]()

## Contributing
The library is currently in testing phase and any contributions are highly
valuable now, you can create issues [here](https://github.com/mohsenSy/dopyapi/issues/new),
read and check the docs [here]().

Also you can read about the internals of the library [here]()
